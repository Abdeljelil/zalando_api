#!/bin/bash
DBUSER="zalando"
DBPW="123456789"
DBNAME="zalando_api"
DBNAME_UNITTEST="zalando_api_unittest"

sudo -u postgres psql -t -c "CREATE USER $DBUSER" 
sudo -u postgres psql -t -c "CREATE DATABASE $DBNAME"
sudo -u postgres psql -t -c "CREATE DATABASE $DBNAME_UNITTEST"
sudo -u postgres psql -t -c "ALTER USER $DBUSER WITH encrypted password '$DBPW'"
sudo -u postgres psql -t -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $DBUSER";
sudo -u postgres psql -t -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME_UNITTEST TO $DBUSER"
