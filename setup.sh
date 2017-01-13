set -e

curl -o virtualenv.tar.gz https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz#md5=44e19f4134906fe2d75124427dc9b716
tar xvf virtualenv.tar.gz
rm -rf virtualenv.tar.gz
python virtualenv-15.1.0/virtualenv.py env
source env/bin/activate
pip install -r requirements.txt

echo """


Run < source env/bin/activate > to activate virtual env


""" 
