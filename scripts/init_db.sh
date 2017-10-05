#!/bin/bash


DBUSER="zalando"
DBPW="123456789"
DBNAME="zalando_api"

sudo -u postgres psql -t -c "CREATE USER $DBUSER"
sudo -u postgres psql -t -c "CREATE DATABASE $DBNAME"
sudo -u postgres psql -t -c "ALTER USER $DBUSER WITH encrypted password '$DBPW'";
sudo -u postgres psql -t -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $DBUSER";

# psql -t -d database_name -c $'SELECT c_defaults FROM user_info WHERE c_uid = \'testuser\';'