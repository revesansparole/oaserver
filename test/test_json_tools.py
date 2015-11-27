import json
from nose.tools import assert_raises, with_setup
from os.path import exists
from os.path import join as pj
import requests_mock
from threading import Timer
from time import sleep
from urllib2 import URLError

from oaserver.json_tools import (get_json, parse_url, post_json,
                                 wait_for_content, wait_for_file)

from .small_tools import ensure_created, rmdir

tmp_dir = "takapouet_json"


def setup_func():
    ensure_created(tmp_dir)


def teardown_func():
    rmdir(tmp_dir)


@with_setup(setup_func, teardown_func)
def test_wait_for_file_raise_error_if_no_file_created():
    assert_raises(UserWarning, lambda: wait_for_file(pj(tmp_dir, "tutu.txt")))


@with_setup(setup_func, teardown_func)
def test_wait_for_file_return_when_file_created():
    tmp_file = pj(tmp_dir, "toto.txt")

    def cr_file():
        with open(tmp_file, 'w') as f:
            f.write("")

    t = Timer(0.3, cr_file)
    t.start()
    assert wait_for_file(tmp_file) == pj(tmp_dir, "toto.txt")


@with_setup(setup_func, teardown_func)
def test_wait_for_file_return_only_when_file_is_closed():
    tmp_file = pj(tmp_dir, "toto.txt")

    def cr_file():
        with open(tmp_file, 'w') as f:
            f.write("before")
            sleep(0.2)
            f.write("after")

    t = Timer(0.2, cr_file)
    t.start()
    assert wait_for_file(tmp_file) == pj(tmp_dir, "toto.txt")
    with open(tmp_file, 'r') as f:
        assert f.read() == "beforeafter"


@with_setup(setup_func, teardown_func)
def test_wait_for_content_remove_file_after_reading():
    tmp_file = pj(tmp_dir, "toto.json")

    def cr_file():
        with open(tmp_file, 'w') as f:
            json.dump("toto", f)
            f.close()

    t = Timer(0.3, cr_file)
    t.start()
    assert wait_for_content(tmp_file) == "toto"
    assert not exists(tmp_file)


def test_parse_url_parse_url():
    url = parse_url("http://domain.com/dir/file.txt")
    assert url.scheme == "http"
    assert url.netloc == "domain.com"
    assert url.path == "/dir/file.txt"


def test_parse_url_default_scheme_is_file():
    url = parse_url("dir/file.txt")
    assert url.scheme == 'file'
    assert url.netloc == ''
    assert url.path == "dir/file.txt"


def test_parse_url_handle_unknown_scheme():
    url = parse_url("code:dir/file.txt")
    assert url.scheme == 'code'
    assert url.netloc == ''
    assert url.path == "dir/file.txt"


def test_parse_url_change_default_scheme():
    url = parse_url("a = 1", 'code')
    assert url.scheme == 'code'
    assert url.path == "a = 1"


def test_parse_url_secure_code():
    url = parse_url("s = 'toto/toto.txt'", 'code')
    assert url.scheme == 'code'
    assert url.path == "s = 'toto/toto.txt'"


@with_setup(setup_func, teardown_func)
def test_get_json_local_raise_error_if_no_file():
    assert_raises(URLError, lambda: get_json(pj(tmp_dir, "toto.tutu")))


@with_setup(setup_func, teardown_func)
def test_get_json_local_raise_error_if_bad_json():
    url = pj(tmp_dir, "toto.json")
    with open(url, 'w') as f:
        f.write("bad data")

    assert_raises(ValueError, lambda: get_json(url))


@with_setup(setup_func, teardown_func)
def test_get_json_local_read_local_file():
    url = pj(tmp_dir, "toto.json")
    data = dict(toto=1)
    with open(url, 'w') as f:
        json.dump(data, f)

    new_data = get_json(url)
    assert id(data) != id(new_data)
    assert data == new_data


@with_setup(setup_func, teardown_func)
def test_get_json_local_handle_different_url_format():
    url = pj(tmp_dir, "toto.json")
    data = dict(toto=1)
    with open(url, 'w') as f:
        json.dump(data, f)

    assert get_json(parse_url("%s" % url)) is not None
    assert get_json("%s" % url) is not None
    assert get_json("file:%s" % url) is not None
    # assert get_json("file:///%s" % url) is not None


@with_setup(setup_func, teardown_func)
def test_get_json_local_handle_bad_url_format():
    assert_raises(URLError, lambda: get_json("file://data"))


@with_setup(setup_func, teardown_func)
def test_get_json_remote_raise_error_if_no_file():
    url = 'http://test.com/'
    with requests_mock.Mocker() as m:
        m.get(url, text="", status_code=500)
        assert_raises(URLError, lambda: get_json(url))


@with_setup(setup_func, teardown_func)
def test_get_json_remote_raise_error_if_bad_json():
    url = 'http://test.com/'
    with requests_mock.Mocker() as m:
        m.get(url, text="bad json")
        assert_raises(ValueError, lambda: get_json(url))


@with_setup(setup_func, teardown_func)
def test_get_json_remote_read_remote_file():
    url = 'http://test.com/'
    data = dict(toto=1)
    with requests_mock.Mocker() as m:
        m.get(url, text=json.dumps(data))

        new_data = get_json(url)
        assert id(data) != id(new_data)
        assert data == new_data


@with_setup(setup_func, teardown_func)
def test_get_json_remote_handle_different_url_format():
    data = dict(toto=1)
    with requests_mock.Mocker() as m:
        for url in ('http://test.com/', 'http://test.com/file.txt'):
            m.get(url, text=json.dumps(data))
            assert get_json(url) is not None


@with_setup(setup_func, teardown_func)
def test_post_json_local_raise_error_if_bad_location():
    url = pj(tmp_dir, "titi", "toto.json")
    assert_raises(URLError, lambda: post_json(url, None))


@with_setup(setup_func, teardown_func)
def test_post_json_local_raise_error_if_non_serializable_data():
    url = pj(tmp_dir, "toto.json")
    myfunc = lambda x: x

    assert_raises(TypeError, lambda: post_json(url, myfunc))


@with_setup(setup_func, teardown_func)
def test_post_json_local_handle_bad_url_format():
    assert_raises(URLError, lambda: post_json("file://data", None))


@with_setup(setup_func, teardown_func)
def test_post_json_local_write_local_file():
    url = pj(tmp_dir, "toto.json")
    data = dict(toto=1)
    post_json(url, data)

    with open(url, 'r') as f:
        new_data = json.load(f)

    assert id(data) != id(new_data)
    assert data == new_data


@with_setup(setup_func, teardown_func)
def test_post_json_local_handle_different_url_format():
    post_json("%s/toto1.json" % tmp_dir, None)
    assert exists(pj(tmp_dir, "toto1.json"))
    post_json("file:%s/toto2.json" % tmp_dir, None)
    assert exists(pj(tmp_dir, "toto2.json"))


@with_setup(setup_func, teardown_func)
def test_post_json_remote_raise_error_if_bad_location():
    url = 'http://krakoukas.schmilblik/'
    assert_raises(URLError, lambda: post_json(url, None))

    with requests_mock.Mocker() as m:
        m.post(url, text="", status_code=500)
        assert_raises(URLError, lambda: post_json(url, None))


@with_setup(setup_func, teardown_func)
def test_post_json_remote_raise_error_if_non_serializable_data():
    url = "http://krakoukas.schmilblik/toto.json"
    myfunc = lambda x: x

    def text_callback(request, context):
        assert False

    with requests_mock.Mocker() as m:
        m.post(url, text=text_callback)
        assert_raises(TypeError, lambda: post_json(url, myfunc))


@with_setup(setup_func, teardown_func)
def test_post_json_remote_write_remote_file():
    url = "http://krakoukas.schmilblik/toto.json"
    data = dict(toto=1)

    def text_callback(request, context):
        new_data = json.loads(request.text)
        assert id(new_data) != id(data)
        assert new_data == data

    with requests_mock.Mocker() as m:
        m.post(url, text=text_callback)
        post_json(url, data)


@with_setup(setup_func, teardown_func)
def test_post_json_remote_handle_different_url_format():
    count = [0]

    def text_callback(request, context):
        count[0] += 1

    with requests_mock.Mocker() as m:
        for url in ('http://test.com/', 'http://test.com/file.txt'):
            m.post(url, text=text_callback)
            post_json(url, None)

    assert count[0] == 2
