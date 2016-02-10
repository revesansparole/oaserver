""" Implement an OA client according to communication protocol
with scifloware specifications to communicate with OAServers.
"""

from time import sleep

from .json_tools import get_json, post_json
from .uos import exists, ls_dir, remove, URLError


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

        for name in ls_dir(self._com_pth):
            pth = self._com_pth + "/" + name
            stdout = pth + "/stdout"
            reg_pth = stdout + "/reg.json"
            try:
                reg = get_json(reg_pth)
                assert reg['type'] == "FileSystemEngine"
                remove(reg_pth)
                args = reg['args']
                self._sid = args['id']
                self._stdout = stdout
                self._compute_pth = pth + "/stdin/" + args["url"]
                self._ping_pth = pth + "/stdin/" + args["urlping"]
                self._delete_pth = pth + "/stdin/" + args["urldelete"]
                return self._sid
            except URLError:
                pass

        return None

    def ping(self, nb_cycles=10):
        """Poll associated server.
        """
        res_pth = self._stdout + "/ping.json"
        if exists(res_pth):
            raise UserWarning("already existing ping answer!!!")

        cmd = dict(url=res_pth)
        post_json(self._ping_pth, cmd)

        for i in range(nb_cycles):
            if exists(res_pth):
                res = get_json(res_pth)
                remove(res_pth)
                assert res['id'] == self._sid
                return res['state']

            sleep(0.1)

        #raise UserWarning("server down")
        return None

    def compute(self, pycode, data):
        """Launch a script on server.

        Notes: this function launch computation and does not wait for an answer.
               You need to ping server until state == 'waiting' and then call
               get_result.

        Args:
            pycode: (str) python code
            data: (dict) keyword arguments for script

        Returns:
            (None)
        """
        if self._sid is None:
            raise UserWarning("No registered server, connect first???")

        res_pth = self._stdout + "/result.json"
        if exists(res_pth):
            raise UserWarning("already existing computation answer!!!")

        data_str = "\n".join("%s = %s" % it for it in data.items())
        cmd = dict(workflow="pycode:" + pycode,
                   urldata=data_str,
                   urlreturn=res_pth)

        post_json(self._compute_pth, cmd)

    def get_result(self):
        """Fetch result of a computation.

        Returns:
            (any) actual result of script call
        """
        res_pth = self._stdout + "/result.json"
        if not exists(res_pth):
            raise UserWarning("Computation still running????")

        res = get_json(res_pth)
        remove(res_pth)
        assert res['id'] == self._sid
        return res['result']

    def kill_server(self):
        """Kill associated server.
        """
        if self._sid is None:
            raise UserWarning("No registered server, connect first???")

        cmd = dict()
        post_json(self._delete_pth, cmd)
