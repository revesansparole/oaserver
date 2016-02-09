"""Generalize os package to remote locations.
"""

import os


def ls(pth):
    """List all files at a given location.

    Args:
        pth: (str) path to check

    Returns:
        (list of str): list of filenames
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
