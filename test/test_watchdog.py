import json
from nose.tools import assert_raises, with_setup
from os import mkdir, remove, rmdir
from os.path import join as pj
from time import sleep

from oaserver.watchdog import Watchdog, WatchdogListener

from .small_tools import ensure_created, rmdir


tmp_dir = "takapouet_uos"
tmp_wpth = pj(tmp_dir, "wpth")
tmp_file = pj(tmp_dir, "toto.txt")
tmp_txt = "lorem ipsum"


def setup_func():
    ensure_created(tmp_dir)
    mkdir(tmp_wpth)
    mkdir(pj(tmp_dir, "tree"))
    mkdir(pj(tmp_dir, "tree", "subdir"))

    with open(tmp_file, 'w') as f:
        f.write(tmp_txt)

    for name in ("doofus0.txt", "doofus1.txt", "subdir/doofus.txt"):
        with open(pj(tmp_dir, "tree", name), 'w') as f:
            f.write(tmp_txt)


def teardown_func():
    rmdir(tmp_dir)


class FlagListener(WatchdogListener):
    def __init__(self):
        WatchdogListener.__init__(self)
        self.flag = None

    def file_created(self, name, data):
        self.flag = name


@with_setup(setup_func, teardown_func)
def test_watchdog_run_separate_thread():
    wd = Watchdog(tmp_wpth, None)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    res = wd.watched_path() == tmp_wpth

    wd.stop()
    assert res


def test_watchdog_raise_error_if_path_do_not_exists():
    assert_raises(OSError, lambda: Watchdog("takapouet", None))


@with_setup(setup_func, teardown_func)
def test_watchdog_raise_error_if_dir_not_empty():
    assert_raises(OSError, lambda: Watchdog(pj(tmp_dir, "tree"), None))


@with_setup(setup_func, teardown_func)
def test_watchdog_catch_file_creation_event():
    l = FlagListener()
    wd = Watchdog(tmp_wpth, l)
    wd.start()

    with open(pj(tmp_wpth, "toto.txt"), 'w') as f:
        json.dump("lorem ipsum", f)

    sleep(0.5)
    wd.stop()

    assert l.flag == "toto.txt"


@with_setup(setup_func, teardown_func)
def test_watchdog_do_not_catch_dir_creation_event():
    l = FlagListener()
    wd = Watchdog(tmp_wpth, l)
    wd.start()
    while not wd.is_running():
        sleep(0.1)

    mkdir(pj(tmp_wpth, "tutu"))

    sleep(0.5)
    wd.stop()
    rmdir(pj(tmp_wpth, "tutu"))

    assert l.flag is None


@with_setup(setup_func, teardown_func)
def test_watchdog_catch_file_multiple_creation_event():
    l = FlagListener()
    wd = Watchdog(tmp_wpth, l)
    wd.start()

    res = []
    for i in range(2):
        with open(pj(tmp_wpth, "toto.txt"), 'w') as f:
            json.dump("lorem ipsum", f)

        sleep(0.5)
        res.append(l.flag == "toto.txt")
        l.flag = None

    wd.stop()
    assert all(res)
