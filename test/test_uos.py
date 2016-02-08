from nose.tools import assert_raises
import os

from oaserver.uos import ls, remove


def test_ls_raise_error_if_pth_is_not_a_directory():
    assert_raises(OSError, lambda: ls("takapouet"))


def test_ls_do_not_list_directories():
    assert "subdir" not in ls("test/test_tree")


def test_ls_list_all_files_in_directory():
    res = ls("test/test_tree")
    assert len(res) == 2
    assert "doofus0.txt" in res
    assert "doofus1.txt" in res


def test_remove_raise_error_if_file_do_not_exists():
    assert_raises(OSError, lambda: remove("tutu.titi"))


def test_remove_raise_error_if_pth_is_dir():
    assert_raises(OSError, lambda: remove("test/test_tree/subdir"))


def test_remove_actually_remove_file():
    pth = "test/test_tree/tmp_doofus.txt"
    with open(pth, 'w') as f:
        f.write("lorem ipsum")

    assert os.path.exists(pth)
    remove(pth)
    assert not os.path.exists(pth)
