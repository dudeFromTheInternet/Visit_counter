import json
import unittest
from unittest.mock import MagicMock
from aiohttp import web
from server import (handle, save_clean_statistics,
                    save_dirty_statistics)


class TestVisitorCounter(unittest.TestCase):
    app = web.Application()
    app.router.add_get('/', handle)

    request = MagicMock()
    request.remote = "127.0.0.1"

    response = app.loop.run_until_complete(app.router['/'].handler(request))
    assert response.status == 200

    def test_save_clean_statistics(self):
        clean_stats_file = "clean_statistics.json"

        visitors_count = 10
        unique_visitors = {'192.168.0.1', '192.168.0.2'}
        visits_by_day = {'2023-11-02': 5}
        save_clean_statistics(
            visitors_count, unique_visitors, visits_by_day, clean_stats_file
        )

        with open(clean_stats_file, 'r') as f:
            data = json.load(f)
            assert data['total_visits'] == visitors_count
            assert set(data['total_unique_visits']) == unique_visitors
            assert data['visits_by_day'] == visits_by_day

    def test_save_dirty_statistics(self):
        dirty_stats_file = "dirty_statistics.json"

        visitors_count = 10
        unique_visitors = {'192.168.0.1', '192.168.0.2'}
        visits_by_day = {'2023-11-02': 5}
        # Предположим, что ваш код записывает данные в файл
        save_dirty_statistics(
            visitors_count, unique_visitors, visits_by_day, dirty_stats_file
        )

        # Проверяем, что файл содержит ожидаемые данные
        with open(dirty_stats_file, 'r') as f:
            data = json.load(f)
            assert data['total_visits'] == visitors_count
            assert set(data['total_unique_visits']) == unique_visitors
            assert data['visits_by_day'] == visits_by_day
