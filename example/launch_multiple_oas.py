from subprocess import Popen

print "multi"
for port in range(6540, 6545):
    Popen(["python", "-i", "launch_rest_server.py", str(port)])
