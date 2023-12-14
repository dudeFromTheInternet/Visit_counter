import json
import unittest
from aiohttp.test_utils import AioHTTPTestCase
from web_app import WebApp
from statistics_collector import StatisticsCollector


class TestWebApp(AioHTTPTestCase):
    async def get_application(self):
        collector = StatisticsCollector('statistics/dirty_statistics.json',
                                        'statistics/clean_statistics.json')
        web_app = WebApp(collector)
        return web_app.app

    async def test_handle(self):
        response = await self.client.get('/')
        self.assertEqual(response.status, 200)
        self.assertIn('text/html', response.headers['Content-Type'])
        self.assertIn('<li>{day}: {visits}</li>', await response.text())

    async def test_get_statistics(self):
        response = await self.client.get('/statistics')
        self.assertEqual(response.status, 200)
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertTrue(json.loads(await response.text()))

    async def test_show_month_statistics(self):
        response = await self.client.get('/show_month_statistics/12')
        self.assertEqual(response.status, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])

    async def test_show_daily_statistics(self):
        response = await self.client.get('/show_daily_statistics/2023-01-01')
        self.assertEqual(response.status, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])

    async def test_show_hourly_statistics(self):
        response = await self.client.get('/show_hourly_statistics/2023-01-01')
        self.assertEqual(response.status, 200)
        self.assertIn('text/plain', response.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
