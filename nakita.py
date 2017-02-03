#!/usr/bin/python2.7

import json
import random

from urllib import urlopen
from urlparse import parse_qs

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Insert your slack slash command token here
slack_token = 'SLACK SLASH COMMAND TOKEN'
# Insert your api token here
api_token = 'SLACK API TOKEN'
api_url = 'https://slack.com/api'


def get_channel_members(channel):
    url = '{}/channels.info?channel={}&token={}'.format(
        api_url, channel, api_token)
    return json.load(urlopen(url))['channel']['members']


def get_group_members(channel):
    url = '{}/groups.info?channel={}&token={}'.format(
        api_url, channel, api_token)
    return json.load(urlopen(url))['group']['members']


def get_user_name(user_id):
    url = '{}/users.info?user={}&token={}'.format(
        api_url, user_id, api_token)
    return json.load(urlopen(url))['user']['name']


class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, retcode=200):
        self.send_response(retcode)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = parse_qs(self.rfile.read(content_length))
        print(post_data)
        if post_data['token'][0] != slack_token:
            self._set_headers(403)
            return
        if post_data['channel_name'][0] == 'privategroup':
            members = get_group_members(post_data['channel_id'][0])
        else:
            members = get_channel_members(post_data['channel_id'][0])
        # TODO: ignores?
        member_id = random.choice(members)
        member = get_user_name(member_id)
        nakki_announce = {
            'response_type': 'in_channel',
            'text': 'Nakita Crushyou has 5 year plan for @{}'.format(member),
            'attachments': [
                {
                    'text': post_data['text'][0]
                }
            ]
        }
        self._set_headers()
        self.wfile.write(json.dumps(nakki_announce))

        
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8123):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting nakita httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
