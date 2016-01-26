from oaserver.oa_client_rest import OAClientRest

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
port = 6544

oac = OAClientRest(sheldon, port)
oac.start()
