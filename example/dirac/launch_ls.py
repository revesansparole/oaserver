from oaserver.uos import ls

com_dir = "/vo.france-grilles.fr/user/j/jchopard"

print ls("dirac:%s" % com_dir)
