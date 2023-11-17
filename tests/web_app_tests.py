import unittest
from aiohttp.test_utils import AioHTTPTestCase
from unittest.mock import Mock, patch
from web_app import WebApp


class TestWebApp(AioHTTPTestCase):
    async def get_application(self):
        collector = Mock()
        return WebApp(collector).app

    async def test_handle(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='mocked_html_content')):
            response = await self.client.get('/')
            self.assertEqual(response.status, 200)
            self.assertEqual(response.content_type, 'text/html')

    async def test_get_statistics(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='mocked_statistics')):
            response = await self.client.get('/statistics')
            self.assertEqual(response.status, 200)
            self.assertEqual(response.content_type, 'text/html')


if __name__ == '__main__':
    unittest.main()
