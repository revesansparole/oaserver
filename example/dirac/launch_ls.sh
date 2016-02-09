#! /bin/bash

#JDL StdError = std.err
#JDL StdOutput = std.out
#JDL OutputSandbox={"std.out","std.err"}
#JDL JobName = test_data
#JDL JobGroup = mytests

dirac-dms-get-file /vo.france-grilles.fr/user/j/jchopard/venv.zip
dirac-dms-get-file /vo.france-grilles.fr/user/j/jchopard/launch_ls.py
unzip -q venv.zip
source venv/bin/activate
venv/bin/python launch_ls.py

