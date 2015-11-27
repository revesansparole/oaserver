""" Set of tools to help server usage
"""

import json
from os import remove
from os.path import abspath, exists
import psutil
import requests
from requests.exceptions import ConnectionError, InvalidSchema
from time import sleep
from urllib2 import URLError
import urlparse
import web


def file_still_in_use(pth):
    """Test whether a file is still used by the system.

    args:
     - pth (str): path of file to check

    return:
     - (bool)
    """
    full_pth = abspath(pth)
    for proc in psutil.process_iter():
        if proc.name().lower() == "python.exe":
            try:
                for handle in proc.open_files():
                    if handle.path == full_pth:
                        return True
            except psutil.AccessDenied:
                pass

    return False


def wait_for_file(pth, nb_cycles=5):
    """ Wait for the creation of a file a given number of cycles.
    Then if file still not created raise UserWarning

    args:
     - pth (str): path to file to watch
     - nb_cycles (int): number of try before raising error
    """
    for i in range(nb_cycles):
        if exists(pth) and not file_still_in_use(pth):
            return pth

        sleep(0.1)

    raise UserWarning("file not created")


def wait_for_content(pth, nb_cycles=5):
    """ Wait for a file to appear, read its content
    then remove it.

    use :func:`wait_for_file`
    args:
     - pth (str): path to file to watch
     - nb_cycles (int): number of try before raising error

    return:
     - (any): any data stored in pth in json format
    """
    wait_for_file(pth, nb_cycles)
    cnt = get_json(pth)
    remove(pth)
    return cnt


def parse_url(url, default_scheme='file'):
    """ Parse url components adding relevant defaults
    if necessary.

    args:
     - url (str): url to parse
     - default_scheme (str): default scheme to use if None in url

    return:
     - (urlparse.SplitResult)
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    if scheme == '':
        scheme = default_scheme

    return urlparse.SplitResult(scheme, netloc, path, query, fragment)


def get_json(url):
    """ Load json coded data from a given url.

    args:
     - url (urlparse.SplitResult): a split url either remote or local

    return
     - (any)
    """
    if type(url) == str or type(url) == unicode:
        url = parse_url(url)

    if url.netloc == '':
        try:
            with open(url.path, 'r') as f:
                txt = f.read()
        except IOError as e:
            raise URLError(e)
    else:
        try:
            resp = requests.get(url.geturl())
        except InvalidSchema as e:
            raise URLError(e)

        if resp.status_code >= 400:
            raise URLError("url does not exists")

        txt = resp.text

    return json.loads(txt)


def post_json(url, data):
    """ Encode data in json format and write it on url.

    args:
     - url (urlparse.SplitResult): a split url either remote or local
     - data (any): must be json serializable
    """
    if type(url) == str or type(url) == unicode:
        url = parse_url(url)

    if url.netloc == '':
        try:
            with open(url.path, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            raise URLError(e)
    else:
        try:
            ret = requests.post(url.geturl(), json.dumps(data),
                                headers={'content-type': 'application/json'})
            if ret.status_code > 400:
                raise URLError("unable to send data")
        except (ConnectionError, InvalidSchema) as e:
            raise URLError(e)


def retrieve_json():
    """ Convenience function for web.py framework
    """
    return json.loads(web.data())
