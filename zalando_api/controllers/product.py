from zalando_api.models.product import ProductModel
from zalando_api.settings import LOG
import asyncio


class ProductController:

    def __init__(self, request):

        self.db = request.app['db']

    async def search(self, limit, query, column, page, sort, direction):

        sql_query = "SELECT %s FROM products" % column

        if query:
            sql_query += " WHERE name LIKE '%{0}%' OR brand LIKE '%{0}%'".format(query)

        # ORDER BY column-names ASC/DESC
        sql_query += " ORDER BY %s %s" % (direction, sort.upper())

        # Pagination in the SQL
        start_record = ((page - 1) * limit)
        sql_query += " OFFSET %d ROWS" % start_record
        sql_query += " FETCH NEXT %d ROWS ONLY" % (start_record + limit)

        LOG.info(sql_query)

        # Run the select query in the database asynchronously
        rows = await self.db.fetch(sql_query)

        # load the data from Record object to dict
        products = []
        for i, row in enumerate(rows):
            product = ProductModel(row, i + 1)
            products.append(product.to_dict())

        LOG.info("%d products have been found" % len(products))

        return products
