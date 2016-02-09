import json
from nose.tools import assert_raises, with_setup
from os.path import exists
from os.path import join as pj
import requests_mock
from threading import Timer
from urllib2 import URLError

from oaserver.json_tools import get_json, post_json, wait_for_content

from .small_tools import ensure_created, rmdir

tmp_dir = "takapouet_json"


def setup_func():
    ensure_created(tmp_dir)


def teardown_func():
    rmdir(tmp_dir)


@with_setup(setup_func, teardown_func)
def test_get_json_raise_error_if_no_file():
    assert_raises(URLError, lambda: get_json(pj(tmp_dir, "toto.tutu")))


@with_setup(setup_func, teardown_func)
def test_get_json_raise_error_if_bad_json():
    url = pj(tmp_dir, "toto.json")
    with open(url, 'w') as f:
        f.write("bad data")

    assert_raises(ValueError, lambda: get_json(url))


@with_setup(setup_func, teardown_func)
def test_get_json_read_local_file():
    url = pj(tmp_dir, "toto.json")
    data = dict(toto=1)
    with open(url, 'w') as f:
        json.dump(data, f)

    new_data = get_json(url)
    assert id(data) != id(new_data)
    assert data == new_data


@with_setup(setup_func, teardown_func)
def test_post_json_raise_error_if_bad_location():
    url = pj(tmp_dir, "titi", "toto.json")
    assert_raises(URLError, lambda: post_json(url, None))


@with_setup(setup_func, teardown_func)
def test_post_json_raise_error_if_non_serializable_data():
    url = pj(tmp_dir, "toto.json")

    def my_func(x):
        return x

    assert_raises(TypeError, lambda: post_json(url, my_func))


@with_setup(setup_func, teardown_func)
def test_post_json_write_local_file():
    url = pj(tmp_dir, "toto.json")
    data = dict(toto=1)
    post_json(url, data)

    with open(url, 'r') as f:
        new_data = json.load(f)

    assert id(data) != id(new_data)
    assert data == new_data


@with_setup(setup_func, teardown_func)
def test_wait_for_content_raise_error_if_no_file_created():
    assert_raises(UserWarning, lambda: wait_for_content(pj(tmp_dir, "tutu.txt")))


@with_setup(setup_func, teardown_func)
def test_wait_for_content_return_when_file_created():
    tmp_file = pj(tmp_dir, "toto.json")

    def cr_file():
        post_json(tmp_file, "data")

    t = Timer(0.1, cr_file)
    t.start()
    assert wait_for_content(tmp_file) == "data"


@with_setup(setup_func, teardown_func)
def test_wait_for_file_return_only_when_file_is_closed():
    tmp_file = pj(tmp_dir, "toto.json")
    big_data = dict((str(i), None) for i in range(10000))
    # use big amount of data to slow down write process

    def cr_file():
        post_json(tmp_file, big_data)

    t = Timer(0.2, cr_file)
    t.start()
    assert wait_for_content(tmp_file) == big_data


@with_setup(setup_func, teardown_func)
def test_wait_for_content_remove_file_after_reading():
    tmp_file = pj(tmp_dir, "toto.json")

    def cr_file():
        post_json(tmp_file, "toto")

    t = Timer(0.1, cr_file)
    t.start()
    assert wait_for_content(tmp_file) == "toto"
    assert not exists(tmp_file)


