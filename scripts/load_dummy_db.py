import asyncio
import json
import asyncpg
from zalando_api import settings

async def import_table(table):

    cnx_uri = 'postgresql://%s:%s@%s/%s' % (
        settings.DBUSER, settings.DBPW, settings.DBHOST, settings.DBNAME_TEST
    )
    conn = await asyncpg.connect(cnx_uri)
    settings.LOG.info("Database connection has been established")

    try:
        await conn.execute("DROP TABLE %s" % table)
        settings.LOG.info("Old table has been dropped")
    except asyncpg.exceptions.UndefinedTableError:
        pass

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS products(
            id serial PRIMARY KEY,
            name text not null,
            image_url text,
            price decimal(8, 2),
            brand text
        )
    ''')

    with open('scripts/dummy_db.sql', "r", encoding='utf-8') as rfile:
        sql = rfile.read()
        await conn.execute(sql)

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(import_table("products"))
