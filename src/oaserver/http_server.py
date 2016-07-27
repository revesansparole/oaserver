from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

from .oa_server import OAServer


# This class will handles any incoming request from
# the browser
class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        print "init", request, client_address, server

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
        if self.path == "/":
            self.wfile.write(json.dumps({"body": None}))
        elif self.path == "/ping":
            self.wfile.write(json.dumps({"body": "ping"}))
        return


# Create a web server and define the handler to manage the
# incoming request
server = HTTPServer(('', 6544), MyHandler)
server._oas = OAServer("oatest")

print 'Started httpserver on port ', 6544

try:
    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
