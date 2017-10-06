#!/bin/bash
DBUSER="zalando"
DBPW="123456789"
DBNAME="zalando_api"
DBNAME_UNITTEST="zalando_api_unittest"

sudo -u postgres createdb -E UTF8 -T template0 --locale=en_US.utf8 $DBNAME
sudo -u postgres createdb -E UTF8 -T template0 --locale=en_US.utf8 $DBNAME_UNITTEST

sudo -u postgres psql -t -c "CREATE USER $DBUSER" 
sudo -u postgres psql -t -c "ALTER USER $DBUSER WITH encrypted password '$DBPW'"
sudo -u postgres psql -t -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $DBUSER";
sudo -u postgres psql -t -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME_UNITTEST TO $DBUSER"
