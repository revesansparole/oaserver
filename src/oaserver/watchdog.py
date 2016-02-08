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

        self._current_content = set(ls(pth))

    def is_running(self):
        """Check whether watchdog still running.

        Returns:
            (bool): True if watchdog stil running
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
            print "alive", self._running
            current = set(ls(self._watched_pth))
            for name in current - self._current_content:
                self._listener.file_created(name)

            self._current_content = current
            sleep(0.2)
