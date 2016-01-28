""" Implement an OA router according to communication protocol
with scifloware specifications to serve as middleware between
 OA clients and OAServers.
"""

# from cPickle import dump, load
# from os.path import exists
from time import sleep
import threading

from .json_tools import post_json, retrieve_json
from .threaded_server import ThreadedServer


class OATask(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.kill = False
        self.running = False

        self._client = client
        self._answer = None

    def task_finished(self, answer):
        self._answer = answer

    def handle_msg(self, msg):
        if self.running:
            return None
        else:
            return msg

    def run(self):
        self.running = True
        while self._answer is None and not self.kill:
            sleep(0.1)

        self.running = False
        self._client.set_answer(self._answer)


class OAPingTask(OATask):
    def __init__(self, client, sids):
        OATask.__init__(self, client)
        self._sids = sids
        self._states = {}

    def handle_msg(self, msg):
        if OATask.handle_msg(self, msg) is not None:
            return msg

        if msg[0] == 'ping':
            sid = msg[1]['id']
            if sid not in self._states:
                self._states[sid] = msg[1]['state']
                if len(self._states) == len(self._sids):
                    self.task_finished(self._states)

                return None

        return msg


class OAComputeTask(OATask):
    def __init__(self, client, sid):
        OATask.__init__(self, client)
        self._sid = sid

    def handle_msg(self, msg):
        if OATask.handle_msg(self, msg) is not None:
            return msg

        if msg[0] == 'compute':
            sid = msg[1]['id']
            if sid == self._sid:
                self.task_finished(msg[1]['result'])
                return None

        return msg


class OAServerConf(object):
    """Small object used to store server config
    """

    def __init__(self):
        self.compute_url = None
        self.ping_url = None
        self.delete_url = None


class OARouter(threading.Thread):
    """ object used to encapsulate communication with multiple OA servers
    and multiple OA clients.
    """
    def __init__(self):
        """ Constructor
        """
        threading.Thread.__init__(self)

        self.address = None
        self.port = None
        self.base_url = None

        self.ping_ans_url = "/ping/"
        self.compute_ans_url = "/compute/"

        self.server_info = {}

        self.ping_ans = {}
        self._msgs = []
        self._dispatch_messages = True
        self._tasks = []

        # initialize with previous session
        # if exists("router_info.pkl"):
        #     with open("router_info.pkl", 'rb') as f:
        #         self.server_info = load(f)

    def set_address(self, address, port):
        self.address = address
        self.port = port
        self.base_url = "http://%s:%d" % (address, port)

    def add_msg(self, msg_type, msg_content):
        self._msgs.append((msg_type, msg_content))

    def add_task(self, task):
        task.start()
        self._tasks.append(task)

    def register_server(self, registration):
        """Store registration of a new OA server.

        args:
         - registration (msg): msg send by OA server once started
        """
        assert registration["type"] == "RestSystemEngine"  # accept only Rest servers for now
        info = registration["args"]

        sid = info['id']
        oas_conf = OAServerConf()
        oas_conf.compute_url = info['url']
        oas_conf.ping_url = info['urlping']
        oas_conf.delete_url = info['urldelete']

        print sid, "registered"

        self.server_info[sid] = oas_conf
        # with open("router_info.pkl", 'wb') as f:
        #     dump(self.server_info, f)

    def run(self):
        while self._dispatch_messages:
            try:
                msg = self._msgs.pop(0)
                for task in self._tasks:
                    if msg is not None:
                        msg = task.handle_msg(msg)
            except IndexError:
                # clean finished tasks
                for i in range(len(self._tasks) - 1, -1, -1):
                    if not self._tasks[i].running:
                        del self._tasks[i]

                sleep(1.0)

    def stop(self):
        for task in self._tasks:
            task._answer = 0  # TODO for debug and test purpose only
            task.kill = True

        self._dispatch_messages = False

    def servers_state(self, client):
        """Ping all available servers and return their state to the client.
        """
        cmd = dict(url=self.base_url + self.ping_ans_url)
        self.add_task(OAPingTask(client, self.server_info.keys()))

        for sid, info in self.server_info.items():
            post_json(info.ping_url, cmd)

    def find_waiting_server(self):
        """Wait until at least one server is 'waiting' and returns
        its id.
        """
        # TODO
        sid = self.server_info.keys()[0]
        info = self.server_info[sid]
        return sid, info

    def compute(self, client, pycode, data):
        """Launch a script on one available server
        """
        sid, info = self.find_waiting_server()

        data_str = "\n".join("%s = %s" % it for it in data.items())
        cmd = dict(workflow="pycode:" + pycode,
                   urldata=data_str,
                   urlreturn=self.base_url + self.compute_ans_url)

        self.add_task(OAComputeTask(client, sid))

        post_json(info.compute_url, cmd)


router = OARouter()
router.start()


class OARDefault(object):
    """ Default task for openalea client
    """
    def GET(self):
        return "OAR was here"

    def POST(self):
        print "OAR received POST"


class OARRegister(object):
    """ Task called to register a OA server
    """
    def POST(self):
        data = retrieve_json()
        router.register_server(data)


class OARPing(object):
    """ Task called to ping state of server
    """
    def POST(self):
        data = retrieve_json()
        router.add_msg('ping', data)


class OARCompute(object):
    """ Task called once server computation is finished
    """
    def POST(self):
        data = retrieve_json()
        router.add_msg('compute', data)


class OARouterRest(ThreadedServer):
    """ REST front end for OA router to communicate with OA servers
    """
    def __init__(self, address, port):
        """ Constructor

        args:
         - sid (str): unique id for this server.
         - oas_descr (str,int): (address, port) of this server
         - sfws_descr (str,int): description of swf server to
                                 communicate with (address, port).
        """
        router.set_address(address, port)

        urls = ('/helloworld/', 'OARDefault',
                '/register/', 'OARRegister',
                router.ping_ans_url, 'OARPing',
                router.compute_ans_url, 'OARCompute')
        ThreadedServer.__init__(self, urls, globals(), address, port)
