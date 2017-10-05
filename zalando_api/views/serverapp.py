import asyncpg
from zalando_api.views.product import search
from zalando_api.views.healthcheck import endpoint
from zalando_api.views.middleware import error_middleware
from zalando_api import settings
from aiohttp import web


async def _open_db_connection(app):

    # Create a database connection pool
    conn = await asyncpg.create_pool(database=settings.DBNAME,
                                     user=settings.DBUSER,
                                     password=settings.DBPW,
                                     host=settings.DBHOST,)

    settings.LOG.debug("Database pool conncection has been established")

    app['db'] = conn


async def _close_db_connection(app):

    await app['db'].close()

def get_app():

    app = web.Application(middlewares=[error_middleware])

    app.router.add_get('/%s/healthcheck' % settings.API_VERSION, endpoint)
    app.router.add_get('/%s/api/search' % settings.API_VERSION, search)

    app.on_startup.append(_open_db_connection)

    app.on_cleanup.append(_close_db_connection)

    return app
