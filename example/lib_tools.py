"""
functions used to discover libraries on a linux system
"""

import fnmatch
import os
import re
import subprocess

from subpro import check_output


def find_libs(root):
    """Iterate on all library files in root arborescence.
    """
    for base, dirs, files in os.walk(root):
        for fname in fnmatch.filter(files, "*.so"):
            yield fname, os.path.join(base, fname)


def lib_parents(lib):
    """Find all library dependencies.

    Use 'ldd'
    """
    ldd_out = check_output(['ldd', lib])
    for line in ldd_out.splitlines():
        match = re.match(r'\t(.*) => (.*) \(0x', line)
        if match:
            yield match.group(1), match.group(2)


def lib_path(lib):
    """Find path of lib on the system.

    returns None if lib not on the system
    Use ldconfig and grep
    """
    try:
        ret = check_output("ldconfig -p | grep %s" % lib, shell=True)
        for line in ret.splitlines():
            match = re.match(r'\t(.*) => (.*)', line)
            if match:
                return match.group(2)
    except subprocess.CalledProcessError:
        return None
    return None


def is_external(lib, root):
    """Check whether lib is inside the given environment.

    root point to the directory base of environment
    """
    lib_pth = os.path.normpath(os.path.abspath(lib))
    env_pth = os.path.normpath(os.path.abspath(root))

    return not lib_pth.startswith(env_pth)


