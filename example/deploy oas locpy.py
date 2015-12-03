####################################################################
#
print "deploy oaserver"
#
####################################################################
from os import environ
environ["PATH"] = "/home/revesansparole/Desktop/dvlpt/locpy/bin:%s" % environ["PATH"]

####################################################################
#
print "use oaserver"
#
####################################################################
from subprocess import call

call("python perform\ computation.py", shell=True, env=environ)
# call("which python", shell=True, env=environ)
