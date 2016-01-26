from oaserver.oa_server_rest import OAServerRest

####################################################################
#
#   launch oaserver
#
####################################################################
address = "193.49.108.153"
# address = "10.0.14.242"
# address = "127.0.0.1"
# address = "147.99.24.168"
port = 6543

oas = OAServerRest("doofus", address, port)
print "registering"
oas.register("http://193.49.108.153:6544/register/")
oas.start()
