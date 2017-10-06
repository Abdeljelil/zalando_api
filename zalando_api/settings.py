import logging

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

API_VERSION = "v1"

# database connection parameters
DBHOST = "localhost"
DBUSER = "zalando"
DBPW = "123456789"

# "zalando_api_unittest" for unittest database
DBNAME = "zalando_api"
DBNAME_TEST = "zalando_api_unittest"

# The number of record will be extracted from zalando api
NB_RECORD = 4000
