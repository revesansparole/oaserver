import json
import requests
from time import sleep


def sw(v):
    return json.dumps(v)


def ping():
    res = requests.post("http://127.0.0.1:6544/ping")
    return res.json()['ans']['state']

# res = requests.post("http://127.0.0.1:6544/ping")
# print res.status_code
# print "res", res.json()


pycode = """
from time import sleep

c = a + b
sleep(5)
"""

data = dict(workflow=sw("pycode:%s" % pycode),
            data=sw(dict(a=1, b=2)),
            outputs=sw(["c"]),
            wtf=sw("here"))

res = requests.post("http://127.0.0.1:6544/compute", data=data)
print "compute", res.status_code
print "res", res.json()

while ping() == "running":
    sleep(0.1)

res = requests.post("http://127.0.0.1:6544/results")
print "resulst", res.status_code
print "res", res.json()
