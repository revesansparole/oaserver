from sys import argv
from oaserver.oa_server_rest import OAServerRest

from ip_list import *

if len(argv) == 1:
    sid = "doofus"
    port = 6543
else:
    port = int(argv[1])
    sid = "doofus:%d" % port

####################################################################
#
#   launch oaserver
#
####################################################################
oas = OAServerRest(sid, localhost, port)
oas.register("http://%s:6539/register/" % localhost)
oas.start()
