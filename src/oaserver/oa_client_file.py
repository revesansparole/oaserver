""" Implement an OA client according to communication protocol
with scifloware specifications to communicate with OAServers.
"""

from os import listdir, remove
from os.path import exists, isdir
from os.path import join as pj
from time import sleep

from oaserver.json_tools import get_json, post_json


class OAClientFile(object):
    """ object used to encapsulate communication with OA server

    Use file system to communicate
    """
    def __init__(self, com_pth):
        """ Constructor
        """
        self._com_pth = com_pth
        self._sid = None
        self._stdout = None
        self._compute_pth = None
        self._ping_pth = None
        self._delete_pth = None

    def clear(self):
        self._sid = None

    def connect(self):
        """Look through com dir to find a registered server
        """
        if self._sid is not None:
            raise UserWarning("Already connected, clear first?")

        for name in listdir(self._com_pth):
            pth = pj(self._com_pth, name)
            if isdir(pth):
                stdout = pj(pth, "stdout")
                if exists(stdout):
                    if exists(pj(stdout, "reg.json")):
                        reg = get_json(pj(stdout, "reg.json"))
                        remove(pj(stdout, "reg.json"))

                        assert reg['type'] == "FileSystemEngine"
                        args = reg['args']
                        self._sid = args['id']
                        self._stdout = stdout
                        self._compute_pth = pj(pth, "stdin", args["url"])
                        self._ping_pth = pj(pth, "stdin", args["urlping"])
                        self._delete_pth = pj(pth, "stdin", args["urldelete"])
                        return self._sid

        return None

    def ping(self):
        """Poll associated server.
        """
        res_pth = pj(self._stdout, "ping.json")
        if exists(res_pth):
            raise UserWarning("already existing ping answer!!!")

        cmd = dict(url=res_pth)
        post_json(self._ping_pth, cmd)

        for i in range(10):
            if exists(res_pth):
                res = get_json(res_pth)
                remove(res_pth)
                assert res['id'] == self._sid
                return res['state']

            sleep(0.1)

        raise UserWarning("server down")

    def compute(self, pycode, data):
        """Launch a script on server

        args:
         - timeout (int): default 10, max number of seconds to wait for answer
        """
        if self._sid is None:
            raise UserWarning("No registered server, connect first???")

        res_pth = pj(self._stdout, "result.json")
        if exists(res_pth):
            raise UserWarning("already existing computation answer!!!")

        data_str = "\n".join("%s = %s" % it for it in data.items())
        cmd = dict(workflow="pycode:" + pycode,
                   urldata=data_str,
                   urlreturn=res_pth)

        post_json(self._compute_pth, cmd)

    def get_result(self):
        res_pth = pj(self._stdout, "result.json")
        if not exists(res_pth):
            raise UserWarning("Computation still running????")

        res = get_json(res_pth)
        remove(res_pth)
        assert res['id'] == self._sid
        return res['result']
