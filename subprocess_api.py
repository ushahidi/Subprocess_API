#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

HOST = 'localhost'
PORT = 8000

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from json import dumps, loads
from subprocess import call
from tempfile import TemporaryFile
from traceback import format_exc

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            request = loads(self.rfile.read(int(self.headers['Content-Length'])))

            if 'stdin' in request:
                stdin = TemporaryFile()
                stdin.write(request['stdin'])
                stdin.seek(0)
            else:
                stdin = None

            stdout = TemporaryFile()
            stderr = TemporaryFile()

            shell = request['shell'] if 'shell' in request else False

            returncode = call(request['args'], stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

            if stdin != None:
                stdin.close()

            stdout.seek(0)
            stderr.seek(0)

            response_code = 200
            response_body = {'returncode': returncode, 'stdout': stdout.read(), 'stderr': stderr.read()}

            stdout.close()
            stderr.close()
        except:
            response_code = 500
            response_body = {'error': format_exc()}

        self.send_response(response_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(dumps(response_body))
        self.wfile.write('\n')

server = HTTPServer((HOST, PORT), HTTPRequestHandler)
server.serve_forever()
