from oaserver.oa_client import OAClient
from oaserver.oa_router import OARouterRest, router

####################################################################
#
#   launch router
#
####################################################################
from ip_list import *
port = 6539

oarr = OARouterRest(localhost, port)
oarr.start()


oac = OAClient(router)

# code to evaluate
pycode = open("script_mini.py", 'r').read()


def lc():
    return oac.compute(pycode, dict(a=10))
