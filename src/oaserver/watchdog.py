"""Simple implementation of a watchdog
"""

from os.path import join as pj
from threading import Thread
from time import sleep

from json_tools import get_json
from .uos import ls, remove


class WatchdogListener(object):
    """Interface for watchdog listener.
    """
    def file_created(self, name, cnt):
        """Notified when a new file is created in the watched directory.

        Args:
            name: (str) name of new file
            cnt: (any) json loaded content of file

        Returns:
            (any)
        """
        raise NotImplemented


class Watchdog(Thread):
    """Watch after a given empty directory and call listener with the content
    of every new created file.
    """
    def __init__(self, pth, listener):
        """Initialize watchdog

        Args:
            pth: (str) path of directory to watch
            listener: (WatchdogListener) listener for messages

        Returns:
            None
        """
        Thread.__init__(self)
        self._watched_pth = pth
        if len(ls(pth)) > 0:
            raise OSError("directory not empty")

        self._listener = listener
        self._running = False

    def watched_path(self):
        """Fetch path watched by this dog.

        Returns:
            (str)
        """
        return self._watched_pth

    def is_running(self):
        """Check whether watchdog still running.

        Returns:
            (bool): True if watchdog still running
        """
        return self._running

    def stop(self):
        """Force thread to stop.

        Returns:
            None
        """
        self._running = False

    def run(self):
        """Main loop, keep checking directory for file creation.

        Warnings: do not call this method directly, use 'start' instead.

        Returns:
            Never
        """
        self._running = True
        while self._running:
            for name in ls(self._watched_pth):
                pth = pj(self._watched_pth, name)
                cnt = get_json(pth)
                remove(pth)
                self._listener.file_created(name, cnt)

            sleep(0.2)
