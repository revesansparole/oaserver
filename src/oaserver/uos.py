"""Generalize os package to remote locations.
"""

import os
import requests
from requests.exceptions import ConnectionError, InvalidSchema
from urllib2 import URLError
import urlparse


def ensure_url(url, default_scheme='file'):
    """Ensure url argument is a valid url

    Args:
        url: (url|str) url to validate
        default_scheme: (str) in the case of str url, default scheme to use

    Returns:
        (urlparse.SplitResult)
    """
    if isinstance(url, urlparse.SplitResult):
        scheme, netloc, path, query, fragment = url
    else:
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)

    if scheme == '':
        scheme = default_scheme

    return urlparse.SplitResult(scheme, netloc, path, query, fragment)


def ls(pth):
    """List all files at a given location.

    Args:
        pth: (str) path to check

    Returns:
        (list of str): list of file names
    """
    names = []
    for name in os.listdir(pth):
        if not os.path.isdir(os.path.join(pth, name)):
            names.append(name)

    return names


def remove(pth):
    """Delete specified file.

    Args:
        pth: (str) path of file to delete

    Returns:
        None
    """
    os.remove(pth)


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
    src = ensure_url(src)
    if src.netloc == '':
        try:
            with open(src.path, 'rb') as f:
                cnt = f.read()
        except IOError as e:
            raise URLError(e)
    else:
        try:
            resp = requests.get(src.geturl())
        except (ConnectionError, InvalidSchema) as e:
            raise URLError(e)

        if resp.status_code >= 400:
            raise URLError("url does not exists")

        cnt = resp.content

    with open(dst, 'wb') as f:
        f.write(cnt)


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
    dst = ensure_url(dst)

    with open(src, 'rb') as f:
        cnt = f.read()

    if dst.netloc == '':
        try:
            with open(dst.path, 'wb') as f:
                f.write(cnt)
        except IOError as e:
            raise URLError(e)
    else:
        try:
            ret = requests.post(dst.geturl(), cnt,
                                headers={'content-type': 'application/json'})  # TODO sort this out
            if ret.status_code > 400:
                raise URLError("unable to send data: %s" % ret.status_code)
        except (ConnectionError, InvalidSchema) as e:
            raise URLError(e)
