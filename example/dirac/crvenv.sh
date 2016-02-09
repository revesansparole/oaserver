virtualenv venv
source venv/bin/activate

cd ..
python setup.py install

cd try
source deactivate

zip venv
