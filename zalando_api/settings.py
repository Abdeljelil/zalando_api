from tornado.log import enable_pretty_logging, logging

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
enable_pretty_logging()

# os.environ['PYTHONASYNCIODEBUG'] = '1'

API_VERSION = "v1"


DBHOST = "localhost"
DBUSER = "zalando"
DBPW = "123456789"
DBNAME = "zalando_api"
