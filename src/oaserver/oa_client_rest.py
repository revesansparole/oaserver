""" Implement an OA client according to communication protocol
with scifloware specifications to communicate with OAServers.
"""
from time import sleep

from .json_tools import post_json, retrieve_json
from .threaded_server import ThreadedServer


class OAClient(object):
    """Client for OA server
    """
    def __init__(self, address, port):
        """ Constructor
        """
        self.address = address
        self.port = port
        self.base_url = "http://%s:%d/" % (address, port)

        self.server_id = None
        self.compute_url = None
        self.ping_url = None
        self.delete_url = None

        self.ping_ans = None

    def store_registration(self, registration):
        """Connect the client to a given OA server.

        args:
         - oas (OAServer): server to connect to

        return:
         - (bool): whether connection is successful or not
        """
        self.server_id = registration['id']
        self.compute_url = registration['url']
        self.ping_url = registration['urlping']
        self.delete_url = registration['urldelete']

        return True

    def ping(self):
        """Ping associated server and return server state.

        return:
         - (str): current server state
        """
        cmd = dict(url=self.base_url + "ping/")
        self.ping_ans = None
        post_json(self.ping_url, cmd)
        while self.ping_ans is None:
            sleep(0.1)

        return self.ping_ans

    # def compute_script(self, pycode, data, url_return):
    #     """Launch execution of pycode on server.
    #
    #     .. note:: function return once computation is launched but not
    #               necessarily finished
    #
    #     args:
    #      - pycode (str): python code to execute,
    #                      must contain some main function
    #      - data (dict of str, any): data to send to the script
    #      - url_return (str): url where oas will write result of computation
    #     """
    #     data_str = "\n".join("%s = %s" % it for it in data.items())
    #     cmd = dict(workflow="pycode:" + pycode,
    #                urldata=data_str,
    #                urlreturn=url_return)
    #     post_json(self.compute_url, cmd)
    #
    #     while exists(self.compute_url):
    #         sleep(0.1)

oac = OAClient()


class OACDefault(object):
    """ Default task for openalea client
    """
    def GET(self):
        print "OAC received GET"
        return "OAC was here"

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
