""" REST implementation of OA server
"""

import threading

from .oa_server import OAServer
from .json_tools import post_json, URLError
from .watchdog import Watchdog, WatchdogListener


class OAServerFile(WatchdogListener):
    """ File front end for OA server.

    Use file system to communicate with the OAServer
    """
    def __init__(self, sid, wpth):
        """Constructor.

        Args:
            sid: (str) unique id for this server.
            wpth: (str) path, directory to watch for commands.

        Returns:
            None
        """
        WatchdogListener.__init__(self)
        self._oas = OAServer(sid)

        self._obs = Watchdog(wpth, self)

        # register
        self._compute_pth = "compute.cmd"
        self._ping_pth = "ping.cmd"
        self._delete_pth = "delete.cmd"

    #########################################################################
    #
    #   watchdog file observer interface
    #
    #########################################################################
    def start(self):
        print("oas %s started, watching %s" % (self._oas.server_id(),
                                               self._obs.watched_path()))
        self._obs.start()

    def stop(self):
        self._obs.stop()

    def join(self):
        self._obs.join()

    def file_created(self, name, cnt):
        if name == self._ping_pth:
            self.ping(cnt)
        elif name == self._compute_pth:
            self.compute(cnt)
        elif name == self._delete_pth:
            self.delete(cnt)
        else:
            print "created", name

    #########################################################################
    #
    #   OAServer interface wrappers
    #
    #########################################################################
    def ping(self, data):
        self._oas.ping(data['url'])

    def compute(self, data):
        args = (data["workflow"],
                data["urldata"],
                data["urlreturn"])

        th = threading.Thread(group=None,
                              target=self._oas.compute,
                              name="OAS.compute",
                              args=args)
        th.start()

    def delete(self, data):
        del data
        self._obs.stop()
        self._oas.delete()

    #########################################################################
    #
    #   registration
    #
    #########################################################################
    def register(self, url_master):
        """Register this worker server to a master.

        Args:
            url_master: (str) url to use to register

        Returns:

        """
        data = {"type": "FileSystemEngine",  # fixed name for SFW protocol
                "args": {
                    "name": "OpenAlea",
                    "id": self._oas.server_id(),
                    "url": self._compute_pth,
                    "urlping": self._ping_pth,
                    "urldelete": self._delete_pth}
                }

        try:
            post_json(url_master, data)
        except URLError:
            raise UserWarning("unable to register with server")

        self._oas.registered()
