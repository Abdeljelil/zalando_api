from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from zalando_api.views.serverapp import get_app
from zalando_api import settings
from aiohttp import web
import json
import logging

logging.basicConfig(level=logging.CRITICAL)
settings.LOG.setLevel(logging.CRITICAL)


class ZalandoApiUnittest(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        return get_app()

    @unittest_run_loop
    async def test_healthcheck_endpoint_200(self):

        request = await self.client.request("GET", "/v1/healthcheck")
        assert request.status == 200
        text = await request.text()
        data = json.loads(text)

        assert data["status"] is True
        assert data["message"] == "running"

    @unittest_run_loop
    async def test_healthcheck_endpoint_503(self):

        await self.app['db'].close()

        request = await self.client.request("GET", "/v1/healthcheck")
        assert request.status == 503
        text = await request.text()
        data = json.loads(text)

        assert data["status"] is False

    @unittest_run_loop
    async def test_middleware_404(self):

        request = await self.client.request("GET", "/v1/wrong/url")
        assert request.status == 404

        text = await request.text()
        data = json.loads(text)
        assert data["error"] == "Not Found"

    @unittest_run_loop
    async def test_get_all_products_200(self):

        request = await self.client.request("GET", "v1/api/search")
        assert request.status == 200

        text = await request.text()
        data = json.loads(text)
        data = data["data"]

        assert len(data) == 10

    @unittest_run_loop
    async def test_wrong_paramaters_number_400(self):

        request = await self.client.request("GET", "v1/api/search?page=i")
        assert request.status == 400

        request = await self.client.request("GET", "v1/api/search?page=0")
        assert request.status == 400

        request = await self.client.request("GET", "v1/api/search?per_page=i")
        assert request.status == 400

        request = await self.client.request("GET", "v1/api/search?per_page=0")
        assert request.status == 400

        request = await self.client.request("GET", "v1/api/search?sort=error")
        assert request.status == 400

    @unittest_run_loop
    async def test_wrong_columns_number_500(self):

        request = await self.client.request("GET", "v1/api/search?c=notfound")
        assert request.status == 500

        text = await request.text()
        data = json.loads(text)

        assert 'error' in data

    @unittest_run_loop
    async def test_query_200(self):

        request = await self.client.request("GET", "v1/api/search?q=jeans")
        assert request.status == 200

        text = await request.text()
        data = json.loads(text)
        data = data["data"]
        for item in data:
            assert "jeans" in item["name"] or "jeans" in item["brand"]
