# Asynchronous restful API with aiohttp and asyncpg

Python web application to expose Zalando products through an asynchronous restful API.

### Prerequisites

This application requires [docker](https://docs.docker.com) package.

### Installing
This application is self contained and easy runnable, the data population and the unittest run as soon as the container is started.

```
sudo docker build -t your_image_name .
sudo docker run -d -p 8080:8080 your_image_name
```
For the foreground mode to watch the unittest logs and the data population steps:
```
sudo docker run -it -p 8080:8080 your_image_name
```

### Running the tests
To run the unittest manually:
```
sudo docker exec -it <the container id> bash
make test
```
output:
```
test_complex_query_page_1_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_complex_query_page_2_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_filter_columns_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_get_all_products_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_healthcheck_endpoint_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_healthcheck_endpoint_503 (tests.test_api.ZalandoApiUnittest) ... ok
test_middleware_404 (tests.test_api.ZalandoApiUnittest) ... ok
test_query_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_sort_asc_brand_direction_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_sort_desc_brand_direction_200 (tests.test_api.ZalandoApiUnittest) ... ok
test_wrong_columns_number_500 (tests.test_api.ZalandoApiUnittest) ... ok
test_wrong_paramaters_number_400 (tests.test_api.ZalandoApiUnittest) ... ok

Name                                  Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------------
zalando_api/__init__.py                   1      0      0      0   100%
zalando_api/controllers/__init__.py       0      0      0      0   100%
zalando_api/controllers/product.py       24      0      8      0   100%
zalando_api/settings.py                  11      0      0      0   100%
zalando_api/views/__init__.py             0      0      0      0   100%
zalando_api/views/healthcheck.py         14      0      0      0   100%
zalando_api/views/middleware.py          21      0      4      0   100%
zalando_api/views/product.py             28      0      8      0   100%
zalando_api/views/serverapp.py           19      0      0      0   100%
-----------------------------------------------------------------------
TOTAL                                   118      0     20      0   100%
----------------------------------------------------------------------
Ran 12 tests in 1.748s
```

### Restful Api services
This application is designed to expose only 4000 products from [Zalando api](https://api.zalando.com/articles).
if you want get more records you should update *NB_RECORD* field in zalando_api/settings.py.
Only one GET service is available through this API */v1/api/search* and the parameters are described in the table bellow.


Parameter | Function | Endpoint
--- | --- | ---
per_page | Limits the maximum number of items per page the query will retrieve. Default 10. | /v1/api/search |
q | full text query to match products by any columns (product name, brand). In case of empty q, all results are return | /v1/api/search?q=jeans |
c | Matches only a particular column. Examples: product, brand | /v1/api/search?q=jeans&c=brand |
page | The page number. Default 1 | /v1/api/search?page=2 |
sort |The way of sorting the products. Options: name, price, brand - Default sorting: price asc| /v1/api/search?sort=name&page=2 |
direction | The direction of sorting. Options: asc or desc | /v1/api/search?page=2&direction=asc |

### Example

```
/v1/api/search?sort=desc&direction=brand&q=Jumper&per_page=5&page=1
```

output

```json
{
    "data": [
        {
            "index": 1,
            "id": 509,
            "name": "Jumper - eventide",
            "image_url": "https://i3.ztat.net/large/Z1/72/1E/02/SK/12/Z1721E02S-K12@12.jpg",
            "price": 16.5,
            "brand": "Zizzi"
        },
        {
            "index": 2,
            "id": 511,
            "name": "Jumper - heather rose",
            "image_url": "https://i5.ztat.net/large/Z1/72/1E/02/SJ/11/Z1721E02S-J11@12.jpg",
            "price": 16.5,
            "brand": "Zizzi"
        },
        {
            "index": 3,
            "id": 1490,
            "name": "Jumper dress - rust",
            "image_url": "https://i1.ztat.net/large/WL/52/1C/07/XO/11/WL521C07X-O11@12.jpg",
            "price": 27.99,
            "brand": "Wallis"
        }
    ]
}
```

### Healthcheck endpoint
This API provides an healthcheck service to check the availability of the web-server and the connection to the database.
It returns status code 200 if everything is running otherwise 503.
Example:
```
/v1/healthcheck
```
```json
{
    "status": true,
    "message": "running"
}
```

### Built With
* [aiohttp](http://aiohttp.readthedocs.io/en/stable/) - Async http client/server framework
* [asyncpg](https://magicstack.github.io/asyncpg/current/) - asyncpg is a database interface library designed specifically for PostgreSQL and Python/asyncio. 
