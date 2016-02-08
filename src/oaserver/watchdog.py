"""Simple implementation of a watchdog
"""

from threading import Thread
from time import sleep

from .uos import ls


class WatchdogListener(object):
    """Interface for watchdog listener.
    """
    def file_created(self, name):
        """Notified when a new file is created in the watched directory.

        Args:
            name: (str) name of new file

        Returns:
            (any)
        """
        del name
        raise NotImplemented


class Watchdog(Thread):
    """Watch after a given directory
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
        self._listener = listener
        self._running = False

        self._current_content = set()

    def stop(self):
        """Force thread to stop.

        Returns:
            None
        """
        self._running = False

    def run(self):
        """Main loop, keep checking directory for file creation

        Returns:
            Never
        """
        if self._running:
            raise UserWarning("Thread already launched")

        self._running = True
        while self._running:
            current = set(ls(self._watched_pth))
            for name in current - self._current_content:
                self._listener.file_created(name)

            self._current_content = current
            sleep(0.2)
