from nose.tools import assert_raises
from os import mkdir, remove, rmdir
from time import sleep

from oaserver.watchdog import Watchdog, WatchdogListener


class FlagListener(WatchdogListener):
    def __init__(self):
        WatchdogListener.__init__(self)
        self.flag = None

    def file_created(self, name):
        self.flag = name


def test_watchdog_run_separate_thread():
    wd = Watchdog("test/wpth", None)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    wd.stop()
    assert True


def test_watchdog_raise_error_if_path_do_not_exists():
    assert_raises(OSError, lambda: Watchdog("takapouet", None))


def test_watchdog_catch_file_creation_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    with open("test/wpth/toto.txt", 'w') as f:
        f.write("lorem ipsum")

    sleep(0.5)
    wd.stop()
    remove("test/wpth/toto.txt")

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


def test_watchdog_do_not_catch_file_modification_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    with open("test/wpth/toto.txt", 'w') as f:
        f.write("lorem ipsum")

    sleep(0.5)
    res1 = l.flag == "toto.txt"
    l.flag = None
    with open("test/wpth/toto.txt", 'w') as f:
        f.write("lorem ipsum" * 2)

    sleep(0.5)
    res2 = l.flag is None

    wd.stop()
    remove("test/wpth/toto.txt")

    for res in (res1, res2):
        assert res


def test_watchdog_catch_file_multiple_creation_event():
    l = FlagListener()
    wd = Watchdog("test/wpth", l)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    res = []
    for i in range(2):
        with open("test/wpth/toto.txt", 'w') as f:
            f.write("lorem ipsum")

        sleep(0.5)
        res.append(l.flag == "toto.txt")
        remove("test/wpth/toto.txt")
        l.flag = None
        sleep(0.3)

    wd.stop()
    assert all(res)


