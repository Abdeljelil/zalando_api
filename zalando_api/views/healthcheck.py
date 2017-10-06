from aiohttp import web

from zalando_api.settings import LOG


async def endpoint(request):

    db = request.app['db']

    # Dummy query to check the database health
    try:
        await db.fetch("SELECT 1")
        response = {"status": True, "message": "running"}
        status = 200
    except Exception as excp:
        LOG.exception(excp)
        message = "type: %s, reason: %s" % (str(type(excp)), str(excp))
        response = {"status": False, "message": message}
        status = 503

    return web.json_response(response, status=status)
