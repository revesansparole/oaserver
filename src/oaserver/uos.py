"""Generalize os package to remote locations.
"""

from os import listdir
from os.path import isdir, join


def ls(pth):
    """List all files at a given location.

    Args:
        pth: (str) path to check

    Returns:
        (list of str): list of filenames
    """
    names = []
    for name in listdir(pth):
        if not isdir(join(pth, name)):
            names.append(name)

    return names
