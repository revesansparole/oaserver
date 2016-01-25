""" Implement an OA client according to communication protocol
with scifloware specifications to communicate with OAServers.
"""
from .json_tools import retrieve_json
from .threaded_server import ThreadedServer


class OACDefault(object):
    """ Default task for openalea client
    """
    def GET(self):
        print "OAC received GET"

    def POST(self):
        print "OAC received POST"


class OACRegister(object):
    """ Task called to register a OA server
    """
    def POST(self):
        data = retrieve_json()
        # data = {"type": "RestSystemEngine",  # fixed name for SFW protocol
        #         "args": {
        #             "name": "OpenAlea",
        #             "id": oa_server.server_id(),
        #             "url": self.base_url + "compute/",
        #             "urlping": self.base_url + "ping/",
        #             "urldelete": self.base_url + "delete/"}
        #         }
        assert data["type"] == "RestSystemEngine"

        args = data["args"]
        print "register", args


class OACPing(object):
    """ Task called to ping state of server
    """
    def POST(self):
        data = retrieve_json()
        print "ping", data


class OAClientRest(ThreadedServer):
    """ REST front end for OA client (scifloware mock)
    """
    def __init__(self, address, port):
        """ Constructor

        args:
         - sid (str): unique id for this server.
         - oas_descr (str,int): (address, port) of this server
         - sfws_descr (str,int): description of swf server to
                                 communicate with (address, port).
        """
        urls = ('/helloworld/', 'OACDefault',
                '/register/', 'OACRegister',
                '/ping/', 'OACPing')
        ThreadedServer.__init__(self, urls, globals(), address, port)
