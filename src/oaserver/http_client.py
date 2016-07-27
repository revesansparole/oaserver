import requests

# res = requests.get("http://127.0.0.1:6544/ping")
# print res.status_code
# print "res", res.json()

res = requests.post("http://127.0.0.1:6544/ping")
print res.status_code
print "res", res.json()
