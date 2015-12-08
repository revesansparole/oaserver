from os import mkdir
from os.path import exists
from shutil import rmtree

from oaserver.json_tools import get_json, post_json
from oaserver.oa_client import OAClient
from oaserver.oa_server_file import OAServerFile

####################################################################
#
#   launch oaserver
#
####################################################################
com_dir = "com_dir"
if not exists(com_dir):
    mkdir(com_dir)

oas = OAServerFile("doofus", com_dir)
oac = OAClient()
oac.connect(oas)

# server is up, running and configured

####################################################################
#
#   perform computations
#
####################################################################
# directory to store results
if not exists("res"):
    mkdir("res")

# code to evaluate
pycode = open("script_mini.py", 'r').read()

# launch jobs
for i in range(3):
    oac.compute_script(pycode, dict(a=i), "res/computation%2d.json" % i)

    # wait for server to be ready using ping commands
    state = 'running'
    while state != 'waiting':
        state = oac.ping()
        print state

    # get result
    res = get_json("res/computation%2d.json" % i)
    print "computation %d:" % i, res

####################################################################
#
#   delete server
#
####################################################################
post_json(oac.delete_url, {})
oas.join()

rmtree(com_dir)
rmtree("res")
