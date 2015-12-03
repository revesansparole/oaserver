####################################################################
#
#   launch oaserver
#
####################################################################
from os import mkdir
from os.path import exists

from oaserver.json_tools import wait_for_content
from oaserver.oa_server_file import OAServerFile

com_dir = "com_dir"
if not exists(com_dir):
    mkdir(com_dir)

oas = OAServerFile("doofus", com_dir)
oas.register("reg.json")
oas.start()

ans = wait_for_content("reg.json")
compute_url = ans['args']['url']
ping_url = ans['args']['urlping']
delete_url = ans['args']['urldelete']

# server is up, running and configured

####################################################################
#
#   perform computations
#
####################################################################
from oaserver.json_tools import get_json, post_json


# directory to store results
if not exists("res"):
    mkdir("res")

# code to evaluate
pycode = """
from time import sleep

def main(a):
    " Emulate some time consuming task"
    sleep(a / 10)
    return a
"""

# launch jobs
for i in range(10):
    # create launch computation command
    cmd = dict(workflow="pycode:" + pycode,
               urldata="a = %d" % i,
               urlreturn="res/computation%2d.json" % i)
    post_json(compute_url, cmd)

    # wait for server to be ready using ping commands
    state = 'running'
    while state != 'waiting':
        cmd = dict(url="pingans.json")
        post_json(ping_url, cmd)
        ans = wait_for_content("pingans.json", 50)
        state = ans['state']
        print state

    # get result
    res = get_json("res/computation%2d.json" % i)
    print "computation %d:" % i, res

####################################################################
#
#   delete server
#
####################################################################
from shutil import rmtree


post_json(delete_url, {})
oas.join()

rmtree(com_dir)
rmtree("res")
