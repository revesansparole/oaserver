virtualenv venv
source venv/bin/activate

cd ../..
python setup.py install

cd example/dirac
deactivate

zip -r venv.zip venv
