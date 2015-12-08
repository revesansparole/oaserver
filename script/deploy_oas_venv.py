from os import chdir, getcwd, mkdir
from os.path import dirname, exists
from os.path import join as pj
from shutil import rmtree
from subprocess import call
import sys


zip_name = sys.argv[1]
venv_dir = dirname(zip_name)

####################################################################
#
print "deploy oaserver"
#
####################################################################
call(["unzip", zip_name])

# relocate venv
cwd = getcwd()
chdir(venv_dir)
execfile("relocate.py")
chdir(cwd)

# start virtual env
act_script = pj(venv_dir, "Scripts", "activate_this.py")
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
if exists(venv_dir):
    rmtree(venv_dir)
