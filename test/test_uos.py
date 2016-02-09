from nose.tools import assert_raises, with_setup
import os
from os.path import join as pj
import requests_mock

from oaserver.uos import get, ls, remove, ensure_url, put, URLError

from .small_tools import ensure_created, rmdir


bad_file = "test/not_supposed_to_be_here.json"
bad_url = "http://toto-hurluberlu.com/myfile.txt"


tmp_dir = "takapouet_uos"
tmp_file = pj(tmp_dir, "toto.txt")
tmp_txt = "lorem ipsum"


def setup_func():
    ensure_created(tmp_dir)
    os.mkdir(pj(tmp_dir, "tree"))
    os.mkdir(pj(tmp_dir, "tree", "subdir"))

    with open(tmp_file, 'w') as f:
        f.write(tmp_txt)

    for name in ("doofus0.txt", "doofus1.txt", "subdir/doofus.txt"):
        with open(pj(tmp_dir, "tree", name), 'w') as f:
            f.write(tmp_txt)


def teardown_func():
    rmdir(tmp_dir)


def test_ensure_url_takes_both_str_and_url():
    url = ensure_url("http://domain.com/dir/file.txt")
    url2 = ensure_url(url)
    assert url == url2


def test_ensure_url_parse_url():
    url = ensure_url("http://domain.com/dir/file.txt")
    assert url.scheme == "http"
    assert url.netloc == "domain.com"
    assert url.path == "/dir/file.txt"


def test_ensure_url_default_scheme_is_file():
    url = ensure_url("dir/file.txt")
    assert url.scheme == 'file'
    assert url.netloc == ''
    assert url.path == "dir/file.txt"


def test_ensure_url_handle_unknown_scheme():
    url = ensure_url("code:dir/file.txt")
    assert url.scheme == 'code'
    assert url.netloc == ''
    assert url.path == "dir/file.txt"


def test_ensure_url_change_default_scheme():
    url = ensure_url("a = 1", 'code')
    assert url.scheme == 'code'
    assert url.path == "a = 1"


def test_ensure_url_secure_code():
    url = ensure_url("s = 'toto/toto.txt'", 'code')
    assert url.scheme == 'code'
    assert url.path == "s = 'toto/toto.txt'"


def test_ls_raise_error_if_pth_is_not_a_directory():
    assert_raises(OSError, lambda: ls("takapouet"))


@with_setup(setup_func, teardown_func)
def test_ls_do_not_list_directories():
    assert "subdir" not in ls(pj(tmp_dir, "tree"))


@with_setup(setup_func, teardown_func)
def test_ls_list_all_files_in_directory():
    res = ls(pj(tmp_dir, "tree"))
    assert len(res) == 2
    assert "doofus0.txt" in res
    assert "doofus1.txt" in res


@with_setup(setup_func, teardown_func)
def test_remove_raise_error_if_file_do_not_exists():
    assert_raises(OSError, lambda: remove("tutu.titi"))


@with_setup(setup_func, teardown_func)
def test_remove_raise_error_if_pth_is_dir():
    assert_raises(OSError, lambda: remove(pj(tmp_dir, "tree/subdir")))


@with_setup(setup_func, teardown_func)
def test_remove_actually_remove_file():
    pth = pj(tmp_dir, "tree", "doofus0.txt")
    assert os.path.exists(pth)
    remove(pth)
    assert not os.path.exists(pth)


@with_setup(setup_func, teardown_func)
def test_get_raise_error_if_src_not_accessible():
    assert_raises(URLError, lambda: get(bad_url, tmp_file))


@with_setup(setup_func, teardown_func)
def test_get_raise_error_if_local_src_not_accessible():
    assert_raises(URLError, lambda: get(bad_file, tmp_file))


@with_setup(setup_func, teardown_func)
def test_get_raise_error_if_dst_not_accessible():
    assert_raises(IOError, lambda: get(tmp_file, "tugudu/data.json"))


@with_setup(setup_func, teardown_func)
def test_get_raise_error_if_no_file():
    url = 'http://test.com/'
    with requests_mock.Mocker() as m:
        m.get(url, text="", status_code=500)
        assert_raises(URLError, lambda: get(url, bad_file))


@with_setup(setup_func, teardown_func)
def test_get_read_local_file():
    pth = pj(tmp_dir, "guiliguili.txt")
    get(tmp_file, pth)
    assert os.path.exists(pth)
    with open(pth, 'r') as f:
        assert f.read().strip() == tmp_txt

    os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_get_read_remote_file():
    url = 'http://test.com/'
    txt = "some data in any format"
    with requests_mock.Mocker() as m:
        m.get(url, text=txt)

        pth = pj(tmp_dir, "tmp_test_file.txt")
        get(url, pth)
        assert os.path.exists(pth)
        with open(pth, 'r') as f:
            assert f.read().strip() == txt

        os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_get_handle_different_url_format():
    txt = "some data in any format"
    with requests_mock.Mocker() as m:
        for url in ('http://test.com/', 'http://test.com/file.txt'):
            m.get(url, text=txt)
            pth = pj(tmp_dir, "tmp_test_file.txt")
            get(url, pth)
            assert os.path.exists(pth)
            with open(pth, 'r') as f:
                assert f.read().strip() == txt

            os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_get_github_url():
    url = "https://raw.githubusercontent.com/revesansparole/oaserver/master/README.rst"
    pth = pj(tmp_dir, "tmp_test_github.txt")
    get(url, pth)
    assert os.path.exists(pth)
    with open(pth, 'r') as f:
        assert "oaserver" in f.read()

    os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_put_raise_error_if_src_not_accessible():
    assert_raises(IOError, lambda: put(bad_file, tmp_file))


@with_setup(setup_func, teardown_func)
def test_put_raise_error_if_dst_not_accessible():
    assert_raises(URLError, lambda: put(tmp_file, bad_url))


@with_setup(setup_func, teardown_func)
def test_put_raise_error_if_local_dst_not_accessible():
    assert_raises(URLError, lambda: put(tmp_file, "tugudu/data.json"))


@with_setup(setup_func, teardown_func)
def test_put_local_write_local_file():

    pth = pj(tmp_dir, "tutu.txt")
    put(tmp_file, pth)

    assert os.path.exists(pth)
    with open(pth, 'r') as f:
        assert f.read().strip() == tmp_txt

    os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_put_local_handle_different_url_format():
    pth = "%s/toto1.json" % tmp_dir
    put(tmp_file, pth)
    assert os.path.exists(pth)
    os.remove(pth)

    pth = "%s/toto2.json" % tmp_dir
    put(tmp_file, "file:%s" % pth)
    assert os.path.exists(pth)
    os.remove(pth)


@with_setup(setup_func, teardown_func)
def test_put_remote_raise_error_if_bad_location():
    url = 'http://krakoukas.schmilblik/'
    assert_raises(URLError, lambda: put(tmp_file, url))

    with requests_mock.Mocker() as m:
        m.post(url, text="", status_code=500)
        assert_raises(URLError, lambda: put(tmp_file, url))


@with_setup(setup_func, teardown_func)
def test_put_remote_write_remote_file():
    url = "http://krakoukas.schmilblik/toto.json"

    def text_callback(request, context):
        del context
        assert request.text.strip() == tmp_txt

    with requests_mock.Mocker() as m:
        m.post(url, text=text_callback)
        put(tmp_file, url)


@with_setup(setup_func, teardown_func)
def test_put_remote_handle_different_url_format():
    count = [0]

    def text_callback(request, context):
        del request
        del context
        count[0] += 1

    with requests_mock.Mocker() as m:
        for url in ('http://test.com/', 'http://test.com/file.txt'):
            m.post(url, text=text_callback)
            put(tmp_file, url)

    assert count[0] == 2
