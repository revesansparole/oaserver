from os import chdir, getcwd, mkdir
from os.path import basename, exists, splitext
from os.path import join as pj
from shutil import rmtree
from subprocess import call
import sys
from time import time


zip_name = sys.argv[1]
venv_dir = splitext(basename(zip_name))[0]

####################################################################
#
print "deploy oaserver"
#
####################################################################
t0 = time()
call(["unzip", zip_name])

# relocate venv
cwd = getcwd()
chdir(venv_dir)
execfile("relocate.py")
chdir(cwd)

# start virtual env
act_script = pj(venv_dir, "bin", "activate_this.py")
execfile(act_script, dict(__file__=act_script))

t1 = time()
####################################################################
#
print "use oaserver"
#
####################################################################
execfile("job.py")

t2 = time()
####################################################################
#
print "clean"
#
####################################################################
if exists(venv_dir):
    rmtree(venv_dir)

t3 = time()
####################################################################
#
print "time"
#
####################################################################
print "deploy", t1 - t0
print "compute", t2 - t1
print "clean", t3 - t2



