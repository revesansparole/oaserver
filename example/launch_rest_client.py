from oaserver.oa_client_rest import OAClientRest, oac

####################################################################
#
#   launch oaserver
#
####################################################################
from ip_list import *
port = 6544

oacs = OAClientRest(sheldon, port)
oacs.start()

pycode = open("script_mini.py", 'r').read()
