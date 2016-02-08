import json
from nose.tools import assert_raises
from os import mkdir, remove, rmdir
from time import sleep

from oaserver.watchdog import Watchdog, WatchdogListener


class FlagListener(WatchdogListener):
    def __init__(self):
        WatchdogListener.__init__(self)
        self.flag = None

    def file_created(self, name, data):
        self.flag = name


def test_watchdog_run_separate_thread():
    wd = Watchdog("test/wpth", None)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    res = wd.watched_path() == "test/wpth"

    wd.stop()
    assert res


def test_watchdog_raise_error_if_path_do_not_exists():
    assert_raises(OSError, lambda: Watchdog("takapouet", None))


def test_watchdog_raise_error_if_dir_not_empty():
    assert_raises(OSError, lambda: Watchdog("test/test_tree", None))


def test_watchdog_catch_file_creation_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()

    with open("test/wpth/toto.txt", 'w') as f:
        json.dump("lorem ipsum", f)

    sleep(0.5)
    wd.stop()

    assert l.flag == "toto.txt"


def test_watchdog_do_not_catch_dir_creation_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    mkdir("test/wpth/tutu")

    sleep(0.5)
    wd.stop()
    rmdir("test/wpth/tutu")

    assert l.flag is None


def test_watchdog_catch_file_multiple_creation_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()

    res = []
    for i in range(2):
        with open("test/wpth/toto.txt", 'w') as f:
            json.dump("lorem ipsum", f)

        sleep(0.5)
        res.append(l.flag == "toto.txt")
        l.flag = None

    wd.stop()
    assert all(res)
