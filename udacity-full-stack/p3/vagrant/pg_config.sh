
apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
pip install GitHub-Flask
pip install ipython
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
# su vagrant -c 'createdb catalog'
# su vagrant -c 'psql catalog -f /vagrant/catalog/catalog.sql'
