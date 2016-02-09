from sys import argv

from oaserver.oa_server_file import OAServerFile
from oaserver.uos import ls, remove

from ip_list import dirac_com_dir as com_dir


if len(argv) == 1:
    sid = "doofus"
else:
    port = int(argv[1])
    sid = "doofus_%d" % port

local_com_dir = com_dir + "/" + sid
stdin = "dirac:%s/stdin" % local_com_dir
stdout = "dirac:%s/stdout" % local_com_dir

for name in ls(stdin):
    remove(stdin + "/" + name)

####################################################################
#
#   launch oaserver
#
####################################################################
oas = OAServerFile(sid, stdin)
oas.register(stdout + "/reg.json")
oas.start()
