from aiohttp import web
from zalando_api.settings import LOG


class BadParametersError(Exception):
    status = 400

    def __init__(self, message):
        self.message = message


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)

        except web.HTTPException as ex:
            LOG.exception(ex)
            return web.json_response(
                {'error': ex.reason}, status=ex.status
            )
        except BadParametersError as badparams:
            LOG.exception(badparams)
            return web.json_response(
                {'error': badparams.message}, status=badparams.status
            )
        except Exception as glex:
            # catch a global exception
            reason = "type: %s, reason: %s" % (str(type(glex)), str(glex))
            LOG.exception(glex)
            return web.json_response({'error': reason}, status=500)

    return middleware_handler
