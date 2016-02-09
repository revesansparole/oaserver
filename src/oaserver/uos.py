"""Generalize os package to remote locations.
"""

import os
import requests
from requests.exceptions import ConnectionError, InvalidSchema
from urllib2 import URLError
import urlparse

import dirac_api


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


def ls(url):
    """List all files at a given location.

    Args:
        url: (url) path to check

    Returns:
        (list of str): list of file names
    """
    url = ensure_url(url)

    if url.netloc != "":
        raise UserWarning("don't know how to handle web ls")

    if url.scheme == "dirac":
        return dirac_api.ls(url)
    else:
        names = []
        for name in os.listdir(url.path):
            if not os.path.isdir(os.path.join(url.path, name)):
                names.append(name)

        return names


def remove(url):
    """Delete specified file.

    Args:
        url: (url) path of file to delete

    Returns:
        None
    """
    url = ensure_url(url)

    if url.netloc != "":
        raise UserWarning("don't know how to handle web ls")

    if url.scheme == "dirac":
        return dirac_api.remove(url)
    else:
        os.remove(url.path)


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
        if src.scheme == "dirac":
            return dirac_api.get(src, dst)
        else:
            try:
                with open(src.path, 'rb') as f:
                    cnt = f.read()

                with open(dst, 'wb') as f:
                    f.write(cnt)
            except IOError as e:
                raise URLError(e)
    else:
        try:
            resp = requests.get(src.geturl())
        except (ConnectionError, InvalidSchema) as e:
            raise URLError(e)

        if resp.status_code >= 400:
            raise URLError("url does not exists")

        with open(dst, 'wb') as f:
            f.write(resp.content)


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

    if dst.netloc == '':
        if dst.scheme == "dirac":
            return dirac_api.put(src, dst)
        else:
            try:
                with open(src, 'rb') as f:
                    cnt = f.read()

                with open(dst.path, 'wb') as f:
                    f.write(cnt)
            except IOError as e:
                raise URLError(e)
    else:
        try:
            with open(src, 'rb') as f:
                cnt = f.read()

            ret = requests.post(dst.geturl(), cnt,
                                headers={'content-type': 'application/json'})  # TODO sort this out
            if ret.status_code > 400:
                raise URLError("unable to send data: %s" % ret.status_code)
        except (ConnectionError, InvalidSchema) as e:
            raise URLError(e)
