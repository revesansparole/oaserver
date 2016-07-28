from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from urlparse import parse_qs

from .oa_server import OAServer


def sw(v):
    return json.dumps(v)


def sr(v):
    return json.loads(v)


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !\nThis is a REST server, use POST only")
        return

    def do_POST(self):
        print "POST: path", self.path
        oas = self.server.oas

        status = None
        ans = None
        if self.path == "/":
            ans = "nothing to do"
        elif self.path == "/ping":
            ans = oas.ping()
        elif self.path == "/compute":
            length = int(self.headers.getheader('content-length'))
            args = parse_qs(self.rfile.read(length), keep_blank_values=1)
            try:
                workflow = sr(args['workflow'][0])
                data = sr(args['data'][0])
                outputs = sr(args['outputs'][0])
                if oas.compute(workflow, data, outputs):
                    status = ('OK', "")
                    ans = oas.ping()
                else:
                    status = ('fail', 'server already computing')
                    ans = {}
            except Exception as e:
                status = (e.__class__.__name__, e.message)
                ans = {}
        elif self.path == "/results":
            status, ans = oas.retrieve_results()

        ret = dict(status=status, ans=ans)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(ret))
        return


def main():
    from sys import argv

    if len(argv) > 1:
        server_name = argv[1]
    else:
        server_name = "oatest"

    server = HTTPServer(('', 6544), MyHandler)
    server.oas = OAServer(server_name)
    server.oas.registered()

    print 'Started httpserver on port ', 6544

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
