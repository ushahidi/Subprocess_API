from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
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

			stdout.seek(0)
			stderr.seek(0)

			response_code = 200
			response_body = {'returncode': returncode, 'stdout': stdout.read(), 'stderr': stderr.read()}
		except:
			response_code = 500
			response_body = {'error': format_exc()}

		self.send_response(response_code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

		self.wfile.write(dumps(response_body))
		self.wfile.write('\n')

server = HTTPServer(('localhost', 8000), HTTPRequestHandler)
server.serve_forever()
