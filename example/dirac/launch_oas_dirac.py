from sys import argv

from oaserver.oa_server_file import OAServerFile
from oaserver.uos import ls, remove

com_dir = "/vo.france-grilles.fr/user/j/jchopard/oas"

if len(argv) == 1:
    sid = "doofus"
else:
    sid = "doofus_%d" % int(argv[1])

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
