from threading import Timer

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
oac2 = OAClient(router)

# code to evaluate
pycode = open("script_mini.py", 'r').read()

def ping1():
    print oac.ping()

def ping2():
    print oac2.ping()

def compute():
    print oac.compute(pycode, dict(a=10))

t1 = Timer(0.1, compute)
t2 = Timer(0.2, ping2)


def lc():
    t1.start()
    t2.start()
