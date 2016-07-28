#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from os import walk
from os.path import abspath, normpath
from os.path import join as pj

from setuptools import setup, find_packages


short_descr = "Server oriented computation for OpenAlea"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/oaserver/version.py
version = {}
with open("src/oaserver/version.py") as fp:
    exec(fp.read(), version)


data_files = []

nb = len(normpath(abspath("src/oaserver_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/oaserver_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


setup_kwds = dict(
    name='oaserver',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole, ",
    author_email="revesansparole@gmail.com, ",
    url='https://github.com/revesansparole/oaserver',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    
    include_package_data=True,
    package_data={'oaserver_data': data_files},
    install_requires=[
        "requests",
        "requests_mock",
        ],
    tests_require=[
        "coverage",
        "flake8",
        "mock",
        "nose",
        "sphinx",
        "coveralls",
        ],
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['console_scripts'] = ['oas = oaserver.http_server:main']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
