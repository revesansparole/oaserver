from os import mkdir
from os.path import exists
from os.path import join as pj
from shutil import rmtree
from sys import argv

from oaserver.oa_server_file import OAServerFile

from ip_list import sheldon_com_dir as com_dir


if len(argv) == 1:
    sid = "doofus"
else:
    port = int(argv[1])
    sid = "doofus_%d" % port

local_com_dir = pj(com_dir, sid)
stdin = pj(local_com_dir, "stdin")
stdout = pj(local_com_dir, "stdout")

if exists(local_com_dir):
    rmtree(local_com_dir, True)

for pth in (com_dir, local_com_dir, stdin, stdout):
    if not exists(pth):
        mkdir(pth)

####################################################################
#
#   launch oaserver
#
####################################################################
oas = OAServerFile(sid, stdin)
oas.register(pj(stdout, "reg.json"))
oas.start()
