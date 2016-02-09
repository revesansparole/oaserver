""" Set of tools to help server usage
"""

import json
from os import remove  # TODO import uos instead
from os.path import exists  # TODO import uos instead
from time import sleep

from oaserver.uos import get, put


def get_json(url):
    """Load json coded data from a given url.

    Args:
        url: (url) either string or url

    Returns:
        (any) data encode in json file
    """
    pth = "tmp_get_json.json"  # TODO better use of random
    get(url, pth)
    with open(pth, 'r') as f:
        data = json.load(f)

    remove(pth)
    return data


def post_json(url, data):
    """Encode data in json format and write it on url.

    Args:
        url: (url) a string or split url either remote or local
        data: (any): must be json serializable

    Returns:
        None
    """
    pth = "tmp_post_json.json"  # TODO better use of random
    with open(pth, 'w') as f:
        json.dump(data, f)

    put(pth, url)
    remove(pth)


def _wait_for_file(pth, nb_cycles=5):
    """Wait for the creation of a file a given number of cycles.

    Raises: UserWarning if file still not created in the end

    Args:
        pth: (str) path to file to watch
        nb_cycles: (int) number of attempts before raising error

    Returns:
        (str) pth
    """
    for i in range(nb_cycles):
        if exists(pth):
            return pth

        sleep(0.1)

    raise UserWarning("file not created")


def wait_for_content(pth, nb_cycles=50):
    """Wait for a file to appear, read its content
    then remove it.

    Args:
        pth: (str) path to file to watch
        nb_cycles: (int) number of attempts before raising error

    Returns:
        (any) any data stored in pth in json format
    """
    _wait_for_file(pth, nb_cycles)
    cnt = get_json(pth)
    remove(pth)
    return cnt
