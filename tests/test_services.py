import unittest
import httpx

from services.gateway.main import app as gateway_app
from services.orchestrator.main import app as orchestrator_app


class ServiceHealthTests(unittest.IsolatedAsyncioTestCase):
    async def request(self, app, path, headers=None):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get(path, headers=headers or {})

    async def test_orchestrator_health_endpoint(self):
        response = await self.request(orchestrator_app, "/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    async def test_gateway_health_endpoint(self):
        response = await self.request(gateway_app, "/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    async def test_gateway_preserves_correlation_id(self):
        response = await self.request(
            gateway_app,
            "/health",
            headers={"X-Correlation-ID": "test-correlation-123"},
        )
        self.assertEqual(response.headers.get("X-Correlation-ID"), "test-correlation-123")


if __name__ == "__main__":
    unittest.main()
