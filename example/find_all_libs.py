""" Script find all library on a system

Excludes tmp directory from search
"""

from pickle import dump

from lib_tools import find_libs

libs = set()

for rep in ("/bin", "/boot", "/dev", "/etc",
            "/home", "/lib", "/lib64", "/opt",
            "/sbin", "/selinux", "/srv", "/sys",
            "/usr", "/var"):
    print(rep)
    for tup in find_libs(rep):
        libs.add(tup)

with open("all_libs.pkl", 'wb') as f:
    dump(libs, f)
