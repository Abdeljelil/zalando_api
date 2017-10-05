from zalando_api import settings
from zalando_api.views.serverapp import get_app
from aiohttp import web


if __name__ == '__main__':

    settings.LOG.info("Starting tornado server on port {}".format(8080))

    web.run_app(get_app(), host='127.0.0.1', port=8080)
