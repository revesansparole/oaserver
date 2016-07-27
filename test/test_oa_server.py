from time import sleep

from oaserver.oa_server import OAServer


pycode = """
from time import sleep

c = a + b
sleep(c / 10.)
"""


def test_server_id_can_be_anything():
    for sid in ("toto", 0, None):
        oas = OAServer(sid)
        assert oas.ping()['id'] == sid


def test_server_state():
    oas = OAServer("toto")
    assert oas.ping()['state'] == "created"

    oas.registered()
    assert oas.ping()['state'] == "waiting"

    # oas.compute("pycode:from time import sleep\nsleep(0.1)", None, None)
    # oas.compute("dummy", 1, None)
    # assert oas.state() == "running"
    # sleep(0.2)
    # assert oas.state() == "waiting"


def test_server_ready_to_compute():
    oas = OAServer("toto")
    assert not oas.compute("toto", {}, [])


def test_server_compute_is_working():
    oas = OAServer("toto")
    oas.registered()

    data = dict(a=1, b=2)
    oas.compute("pycode:%s" % pycode, data, ["c"])
    assert oas.ping()['state'] == "running"
    while oas.ping()['state'] != "waiting":
        sleep(0.1)

    status, res = oas.retrieve_results()
    assert status[0] == 'OK'
    assert res['c'] == 3


def test_server_delete():
    oas = OAServer("toto")
    oas.registered()

    oas.delete()
    assert oas.ping()['state'] == "deleted"
