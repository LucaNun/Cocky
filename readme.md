sudo apt install mariadb-server

python -v venv venv_cocky

source venv_cocky/bin/activate

## Needed for flask-mysqldb
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

pip install flask

pip install Flask-MySQLdb

## Needed for hx711
pip install Rpi.GPIO numpy
