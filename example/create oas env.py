
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys


venv_dir = "oaenv"

if "win" in sys.platform:
    bin_dir = "Scripts"
else:
    bin_dir = "bin"


# create virtual env
try:
    if exists(venv_dir):
        rmtree(venv_dir)

except OSError:
    print("unable to create dir")
    sys.exit(0)

call("virtualenv %s" % venv_dir, shell=True)

execfile("%s/%s/activate_this.py" % (venv_dir, bin_dir),
         dict(__file__="%s/%s/activate_this.py" % (venv_dir, bin_dir)))

# install requirements
reqs = ["openalea.container", "openalea.workflow", "oaserver"]
for name in reqs:
    call("pip install %s" % name)

