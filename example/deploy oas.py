####################################################################
#
print "deploy oaserver"
#
####################################################################
from os import chdir, getcwd, mkdir
from os.path import exists
from os.path import join as pj
import sys
from zipfile import ZipFile


if "win" in sys.platform:
    bin_dir = "Scripts"
else:
    bin_dir = "bin"


venv_dir = "venv_oas"
if not exists(venv_dir):
    mkdir(venv_dir)

# # extract archive into venv
with ZipFile("oas.zip", 'r') as ziph:
    ziph.extractall(venv_dir)

# relocate venv
cwd = getcwd()
chdir(venv_dir)
execfile("relocate.py")
chdir(cwd)

# start virtual env
act_script = pj(venv_dir, bin_dir, "activate_this.py")
execfile(act_script, dict(__file__=act_script))

####################################################################
#
print "use oaserver"
#
####################################################################
execfile("perform computation.py")


####################################################################
#
print "clean"
#
####################################################################
from shutil import rmtree

if exists(venv_dir):
    rmtree(venv_dir)
