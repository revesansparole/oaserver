"""This file contains the common api to access resources
"""
import os
from subprocess import check_output, CalledProcessError
from urllib2 import URLError
from urlparse import SplitResult


def ls(url):
    """List all available resources at the given location

    Warnings: work only on directory like resources.

    Args:
        url: (urlparse.SplitResult) Resource locator

    Returns:
        (list of str): list of resources names.
    """
    root = url.path
    res = check_output(["dirac-dms-find-lfns Path=%s" % root], shell=True)

    pths = set()

    for line in res.splitlines()[1:]:
        line = line.strip()
        if len(line) > 0:
            if line.startswith(root):
                pth = line[len(root):][1:]
                dname = os.path.dirname(pth)
                if len(dname) == 0:
                    pths.add(pth)
            else:
                raise URLError("bad path")

    return pths


def exists(url):
    """Check the existence of a resource.

    Args:
        url: (urlparse.SplitResult) Resource locator

    Returns:
        (Bool): True if resource is accessible
    """
    if url.path[-1] == "/":  # bad way of checking if it is a directory
        root, dname = os.path.split(url.path[:-1])
        root_url = SplitResult(url.scheme, url.netloc, root, url.query, url.fragment)
        return any(name == dname for name, isdir in ls(root_url))
    else:
        res = check_output(["dirac-dms-data-size %s" % url.path], shell=True)
        return not res.startswith("Failed")


def remove(url):
    """Remove a resource.

    Warnings: recursive operation on directory like resources.

    Args:
        url: (urlparse.SplitResult) Resource locator

    Returns:
        (Bool): operation has been successful
    """
    if url.path[-1] == "/":  # bad way of checking if it is a directory
        raise NotImplementedError
    else:
        res = check_output(["dirac-dms-remove-files %s" % url.path], shell=True)
        return res.startswith("Successfully")


def get(src, dst):
    """Retrieve file from remote location and copy it locally

    Raises: URLError if remote location (src) is not accessible

    Raises: IOError if dst is not reachable

    Args:
        src: (url) remote url
        dst: (str) local path

    Returns:
        None
    """
    cwd = os.getcwd()
    src_name = os.path.basename(src.path)
    dst_dir, dst_name = os.path.split(dst)
    if dst_dir == "":
        dst_dir = "."

    os.chdir(dst_dir)
    try:
        res = check_output(["dirac-dms-get-file %s" % src.path], shell=True)
        if res.startswith("ERROR Failed"):
            os.chdir(cwd)
            raise URLError("unable to fetch given resource")

        if dst_name != "" and src_name != dst_name:
            os.rename(src_name, dst_name)

    except CalledProcessError as e:
        raise URLError(e)
    finally:
        os.chdir(cwd)


def put(src, dst):
    """Copy a file from local source to remote location

    Raises: IOError if src is not reachable

    Raises: URLError if remote location (dst) is not accessible

    Args:
        src: (str) local path
        dst: (url) remote url

    Returns:
        None
    """
    try:
        if exists(dst):
            remove(dst)

        res = check_output(["dirac-dms-add-file %s %s DIRAC-USER" % (dst.path, src)], shell=True)
        lines = res.splitlines()
        return lines[-1].startswith("Successfully")
    except CalledProcessError:
        return False
