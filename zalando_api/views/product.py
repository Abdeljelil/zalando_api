from aiohttp import web

from zalando_api.controllers.product import ProductController
from zalando_api.views.middleware import BadParametersError


async def search(request):

    # Track the work flow of a request by create a controller \
    # object for each request
    controller = ProductController(request)

    # Read query parameters
    try:
        limit = int(request.GET.get('per_page', 10))
    except ValueError:
        raise BadParametersError("'per_page' should be an integer type")

    if limit <= 0:
        raise BadParametersError("'per_page' parameter should be great than 0")

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise BadParametersError("'page' should be an integer type")

    if page <= 0:
        raise BadParametersError("'page' parameter should be great than 0")

    sort = request.GET.get('sort', 'asc')

    if sort.upper() not in ['ASC', 'DESC']:
        raise BadParametersError(
            "'sort' parameter should be in {'ASC', 'DESC'}")

    direction = request.GET.get('direction', 'price')

    if direction not in ["name", "price", "brand"]:
        raise BadParametersError(
            "'direction' should be in ['name', 'price', 'brand']")

    query = request.GET.get('q', None)
    column = request.GET.get('c', "*")

    # get the data from the database according the given parameters
    products = await controller.search(
        limit=limit,
        query=query,
        column=column,
        page=page,
        sort=sort,
        direction=direction
    )

    # Convention for the restful api pagination
    headers = {
        'X-Pagination-Count': str(len(products)),
        'X-Pagination-Page': str(page),
        'X-Pagination-Limit': str(limit)
    }

    return web.json_response({"data": products}, headers=headers)
