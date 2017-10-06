import asyncio
import json

import aiohttp
import async_timeout
import asyncpg

from zalando_api import settings

ZALANDO_API_URL = "https://api.zalando.com/"


def parse_raw_products(data):

    if "content" not in data:
        settings.LOG.error(data)
        return []

    products = []
    # Extract only the fields those will be added in the database
    for item in data["content"]:
        image = item["media"]["images"][0]["largeUrl"]
        price = item["units"][0]["price"]["value"]
        products.append(dict(
            name=item["name"],
            image_url=image,
            price=price,
            brand=item["brand"]["name"]
        ))
    return products


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            text = await response.text()
            return json.loads(text)


async def get_products_list():

    products = []

    async with aiohttp.ClientSession() as session:
        pages = (settings.NB_RECORD / 200) + 1
        pages = int(round(pages))
        for page in range(1, pages):
            url = "%sarticles/?page=%d&pageSize=200" % (ZALANDO_API_URL, page)
            settings.LOG.info(url)
            data = await fetch(session, url)
            products += parse_raw_products(data)

    return products


async def populate_db(dbname, dbhost, user, password):

    # Read the products list from zalando api

    products = await get_products_list()
    settings.LOG.info("%d Products loaded from Zalando api" % len(products))

    # Establish a connection
    cnx_uri = 'postgresql://%s:%s@%s/%s' % (user, password, dbhost, dbname)
    conn = await asyncpg.connect(cnx_uri)
    settings.LOG.info("Database connection has been established")

    # Clean up the table
    try:
        await conn.execute("DROP TABLE products")
        settings.LOG.info("Old products table has been dropped")
    except asyncpg.exceptions.UndefinedTableError:
        pass

    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS products(
            id serial PRIMARY KEY,
            name text not null,
            image_url text,
            price decimal(8, 2),
            brand text
        )
    ''')

    # Insert a record into the products table.
    insert_query = '''
        INSERT INTO products(name, image_url, price, brand) VALUES($1, $2, $3, $4)
    '''

    for product in products:
        await conn.execute(
            insert_query, product["name"], product[
                "image_url"], product["price"], product["brand"]
        )

    # Close the connection.
    await conn.close()

if __name__ == "__main__":

    cortourine = populate_db(dbname=settings.DBNAME,
                             user=settings.DBUSER,
                             password=settings.DBPW,
                             dbhost=settings.DBHOST,)

    asyncio.get_event_loop().run_until_complete(cortourine)
