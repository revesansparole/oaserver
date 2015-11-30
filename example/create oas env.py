
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys


venv_dir = "oaenv"


# create virtual env
try:
    if exists(venv_dir):
        rmtree(venv_dir)

except OSError:
    print("unable to create dir")
    sys.exit(0)

call("virtualenv %s" % venv_dir, shell=True)

execfile("%s/Scripts/activate_this.py" % venv_dir,
         dict(__file__="%s/Scripts/activate_this.py" % venv_dir))

# install requirements
reqs = ["openalea.container", "openalea.workflow", "oaserver"]
for name in reqs:
    call("pip install %s" % name)

