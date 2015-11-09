"""
Helper module for creating servers
"""


import threading
import web
from web.httpserver import WSGIServer, StaticMiddleware, LogMiddleware


class ThreadedServer(threading.Thread):
    """Simple wrapper to run a web server in a concurrent thread.
    """
    def __init__(self, matching, namespace, address, port):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.address = address
        self.port = port

        app = web.application(matching, namespace)
        func = app.wsgifunc()
        func = StaticMiddleware(func)
        # func = LogMiddleware(func)

        self.server = WSGIServer((address, port), func)

    def run(self):
        # if self.server.ssl_adapter:
        #     print "\nlaunched: https://%s:%d/" % (self.address, self.port)
        # else:
        print "\nlaunched: http://%s:%d/" % (self.address, self.port)
        self.server.start()

    def stop(self):
        self.server.stop()
