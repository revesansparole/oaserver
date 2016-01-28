from os import mkdir
from os.path import exists
from time import sleep

from oaserver.oa_client_file import OAClientFile

from ip_list import com_dir

if not exists(com_dir):
    mkdir(com_dir)

oac = OAClientFile(com_dir)
con = oac.connect()
print "con", con

if con is not None:
    ping = oac.ping()
    print "ping", ping

    # code to evaluate
    pycode = open("script_mini.py", 'r').read()
    oac.compute(pycode, dict(a=1))
    while oac.ping() != 'waiting':
        sleep(0.2)

    print "res", oac.get_result()

