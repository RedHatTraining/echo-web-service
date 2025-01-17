#!/usr/bin/env python
#
#  Copyright (c) 2021 Red Hat, Inc.  <bowe@redhat.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
"""
__author__ = 'RHT Platform <gls-platform@redhat.com>'
__docformat__ = 'restructuredtext'

import logging
import os
import json
from http.server import HTTPServer
# from http.server import ThreadingHttpServer
from http.server import BaseHTTPRequestHandler

LOG = logging.getLogger(__name__)


class EchoHandler(BaseHTTPRequestHandler):

    def as_dict(self):
        return {
            'client_address': list(self.client_address),
            'servrer': str(self.server),
            'requestline': self.requestline,
            'command': self.command,
            'path': self.path,
            'headers': dict(self.headers),
            'sys_version': self.sys_version,
            'server_version': self.server_version,
            'protocol_version': self.protocol_version,
        }

    def do_any(self):
        text = json.dumps(self.as_dict(), sort_keys=True, indent=2) + "\n"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(text.encode())

    do_GET = do_any
    do_POST = do_any


def main():

    port = os.environ.get("ECHO_WEBAPP_PORT", "8000")

    # handle kubernetes supplied envvars of form
    # tcp://ipaddr:port
    port = port.split(":")[-1]

    server_address = ('', int(port))
    LOG.info(f"echo server binding to port {port}")
    httpd = HTTPServer(server_address, EchoHandler)
    httpd.serve_forever()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    main()
