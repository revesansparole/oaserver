from oaserver.oa_client_rest import OAClientRest

####################################################################
#
#   launch oaserver
#
####################################################################
address = "193.49.108.153"
# address = "10.0.14.242"
# address = "127.0.0.1"
# address = "147.99.24.168"
port = 6544

oac = OAClientRest(address, port)
oac.start()
