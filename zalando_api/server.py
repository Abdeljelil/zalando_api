import sys
from aiohttp import web

from zalando_api import settings
from zalando_api.views.serverapp import get_app

if __name__ == '__main__':

    port = 8080
    host = '0.0.0.0'

    if len(sys.argv) > 1:
        args = sys.argv[1].split(":")
        host = args[0]
        port = int(args[1])

    settings.LOG.info("Starting http server on {}:{}".format(host, port))

    web.run_app(get_app(), host=host, port=port)
