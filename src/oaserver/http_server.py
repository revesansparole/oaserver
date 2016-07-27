from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

from .oa_server import OAServer


# This class will handles any incoming request from
# the browser
class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        print "init", request, client_address, server
        self._oas = server.oas
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !\nThis is a REST server, use POST only")
        return

    def do_POST(self):
        print "POST: path", self.path
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        ans = None
        if self.path == "/":
            ans = "nothing to do"
        elif self.path == "/ping":
            ans = self._oas.ping()

        self.wfile.write(json.dumps(ans))
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
