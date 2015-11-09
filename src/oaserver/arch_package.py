"""
Script used to archivate the current virtual environment into a form
suitable for later de archivating.

Does not work with develop mode of installed packages
"""

from os import chdir, getcwd, walk
from os.path import basename
from os.path import join as pj
import shutil
import sys
import tempfile
from zipfile import ZipFile

import data_access


def main():
    # parse arguments
    output_name = sys.argv[1]

    # find current virtual env
    if not hasattr(sys, 'real_prefix'):
        raise UserWarning("Need to be run from an activated virtualenv")

    vname = basename(sys.prefix)
    vroot = sys.prefix

    # find missing libs
    missing_libs = []

    # copy everything in local temporary dir
    tmp_dir = tempfile.mkdtemp()
    tmp_root = pj(tmp_dir, vname)

    # copy virtualenv
    shutil.copytree(vroot, tmp_root)

    # copy relocate
    with open(pj(tmp_root, "relocate.py"), 'w') as f:
        f.write(data_access.get("relocate.py"))

    # add missing libs
    for lib_pth in missing_libs:
        shutil.copy(lib_pth, pj(tmp_root, "lib", "lib"))

    # zip everything
    cwd = getcwd()
    chdir(tmp_dir)
    with ZipFile(pj(cwd, output_name), 'w') as ziph:
        for root, dirs, files in walk(vname):
            for name in files:
                ziph.write(pj(root, name))

    chdir(cwd)
    shutil.rmtree(tmp_dir)
