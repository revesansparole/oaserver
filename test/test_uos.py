from nose.tools import assert_raises

from oaserver.uos import ls


def test_ls_raise_error_if_pth_is_not_a_directory():
    assert_raises(OSError, lambda: ls("takapouet"))


def test_ls_do_not_list_directories():
    assert "subdir" not in ls("test/test_tree")


def test_ls_list_all_files_in_directory():
    res = ls("test/test_tree")
    assert len(res) == 2
    assert "doofus0.txt" in res
    assert "doofus1.txt" in res
