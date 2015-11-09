""" Set of tools to help server usage
"""

import json
import requests
from requests.exceptions import ConnectionError, InvalidSchema
from urllib2 import URLError
import urlparse
import web


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
