"""
try to relocate a virtualenv
usage
create virtualenv
install stuff

copy virtualenv directory to new location
launch relocate from new root dir of virtualenv
python relocate.py
"""

import os
import stat

root = os.getcwd()

print(root)

# modify shebang line of scripts in bin
# scripts are all files that start with shebang #! .../python
print("shebang")

for fname in os.listdir("bin/"):
    pth = os.path.join("bin", fname)
    if not os.path.islink(pth):
        with open(pth, 'rb') as f:
            header = f.readline()
            data = f.read()
            f.close()
            if header.startswith("#!") and "python" in header:
                with open(pth, 'wb') as f:
                    f.write("#! %s/bin/python\n" % root)
                    f.write(data)
                    f.close()

# create inve bash file
print("inve")

txt = """#!/bin/sh
export VIRTUAL_ENV="%s"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib/lib"
unset PYTHON_HOME

PS1="(`basename \"$VIRTUAL_ENV\"`)[\u@\h \W]\$"
export PS1

exec "${@:-$SHELL}"
""" % root

with open("bin/inve", 'w') as f:
    f.write(txt)
    f.close()
    os.chmod("bin/inve", 0775)
