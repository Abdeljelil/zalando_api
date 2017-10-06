import json
import logging

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from zalando_api import settings
from zalando_api.views.serverapp import get_app

logging.basicConfig(level=logging.CRITICAL)
settings.LOG.setLevel(logging.CRITICAL)


class ZalandoApiUnittest(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        settings.DBNAME = settings.DBNAME_TEST

        return get_app()

    @unittest_run_loop
    async def test_healthcheck_endpoint_200(self):

        request = await self.client.request("GET", "/v1/healthcheck")
        self.assertEqual(request.status, 200)
        text = await request.text()
        data = json.loads(text)

        self.assertTrue(data["status"])
        assert data["message"] == "running"

    @unittest_run_loop
    async def test_healthcheck_endpoint_503(self):

        await self.app['db'].close()

        request = await self.client.request("GET", "/v1/healthcheck")
        self.assertEqual(request.status, 503)
        text = await request.text()
        data = json.loads(text)

        self.assertFalse(data["status"])

    @unittest_run_loop
    async def test_middleware_404(self):

        request = await self.client.request("GET", "/v1/wrong/url")
        self.assertEqual(request.status, 404)

        text = await request.text()
        data = json.loads(text)
        self.assertEqual(data["error"], "Not Found")

    @unittest_run_loop
    async def test_get_all_products_200(self):

        request = await self.client.request("GET", "v1/api/search")
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        assert len(data) == 10

    @unittest_run_loop
    async def test_wrong_paramaters_number_400(self):

        request = await self.client.request("GET", "v1/api/search?page=i")
        self.assertEqual(request.status, 400)

        request = await self.client.request("GET", "v1/api/search?page=0")
        self.assertEqual(request.status, 400)

        request = await self.client.request("GET", "v1/api/search?per_page=i")
        self.assertEqual(request.status, 400)

        request = await self.client.request("GET", "v1/api/search?per_page=0")
        self.assertEqual(request.status, 400)

        request = await self.client.request("GET", "v1/api/search?sort=error")
        self.assertEqual(request.status, 400)

        request = await self.client.request("GET", "v1/api/search?direction=image_url")
        self.assertEqual(request.status, 400)

    @unittest_run_loop
    async def test_wrong_columns_number_500(self):

        request = await self.client.request("GET", "v1/api/search?c=notfound")
        self.assertEqual(request.status, 500)

        text = await request.text()
        data = json.loads(text)

        self.assertIn('error', data)

    @unittest_run_loop
    async def test_query_200(self):

        request = await self.client.request("GET", "v1/api/search?q=jeans")
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]
        for item in data:
            assert "jeans" in item["name"] or "jeans" in item["brand"]

    @unittest_run_loop
    async def test_filter_columns_200(self):

        request = await self.client.request("GET", "v1/api/search?c=brand")
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        allowed_fields = sorted(["index", "brand"])
        for item in data:
            keys = sorted(item.keys())
            self.assertEqual(keys, allowed_fields)

    @unittest_run_loop
    async def test_sort_desc_brand_direction_200(self):

        request = await self.client.request("GET", "/v1/api/search?sort=desc&direction=brand&q=trousers")
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        data = sorted(data, key=lambda x: x["index"])


        expectation = ['Reebok', 'LEGO Wear', 'LEGO Wear',
                       'LEGO Wear', 'LEGO Wear', 'Escada Sport',
                       'Columbia', 'Carhartt WIP', 'adidas Performance']
        print("*" * 50)
        print([x["brand"] for x in data])
        print([x["id"] for x in data])
        print([x["index"] for x in data])
        print("*" * 50)
        self.assertEqual(
            expectation,
            [x["brand"] for x in data]
        )

    @unittest_run_loop
    async def test_sort_asc_brand_direction_200(self):

        request = await self.client.request("GET", "/v1/api/search?sort=asc&direction=brand&q=trousers")
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        data = sorted(data, key=lambda x: x["index"])
        expectation = ['adidas Performance', 'Carhartt WIP',
                       'Columbia', 'Escada Sport', 'LEGO Wear', 'LEGO Wear',
                       'LEGO Wear', 'LEGO Wear', 'Reebok']


        self.assertEqual(
            expectation,
            [x["brand"] for x in data]
        )

    @unittest_run_loop
    async def test_complex_query_page_1_200(self):

        url = '/v1/api/search?sort=desc&direction=brand&q=Jumper&per_page=50&page=1&c=name,brand,price'
        request = await self.client.request("GET", url)
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        self.assertEqual(len(data), 50)

        allowed_fields = sorted(["index", "brand", 'name', 'price'])
        for item in data:
            keys = sorted(item.keys())
            self.assertEqual(keys, allowed_fields)

    @unittest_run_loop
    async def test_complex_query_page_2_200(self):

        url = '/v1/api/search?sort=desc&direction=brand&q=Jumper&per_page=50&page=2&c=name,brand,price'
        request = await self.client.request("GET", url)
        self.assertEqual(request.status, 200)

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        self.assertEqual(len(data), 28)

        allowed_fields = sorted(["index", "brand", 'name', 'price'])
        for item in data:
            keys = sorted(item.keys())
            self.assertEqual(keys, allowed_fields)
