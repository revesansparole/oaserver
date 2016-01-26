from oaserver.oa_server_rest import OAServerRest

####################################################################
#
#   launch oaserver
#
####################################################################
sheldon = "193.49.108.153"
mango = "193.49.108.148"
sheldon_inra = "10.0.14.242"
localhost = "127.0.0.1"
modulor = "147.99.24.168"
port = 6543

oas = OAServerRest("doofus", mango, port)
print "registering"
oas.register("http://%s:6544/register/" % sheldon)
oas.start()
