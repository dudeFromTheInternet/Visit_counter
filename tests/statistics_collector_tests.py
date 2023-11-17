import json
import os
import unittest
from statistics_collector import StatisticsCollector


class TestStatisticsCollector(unittest.TestCase):

    def setUp(self):
        self.dirty_file = 'test_dirty_statistics.json'
        self.clean_file = 'test_clean_statistics.json'
        self.collector = StatisticsCollector(self.dirty_file, self.clean_file)

    def tearDown(self):
        # Очистка тестовых файлов после завершения тестов
        try:
            os.remove(self.dirty_file)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.clean_file)
        except FileNotFoundError:
            pass

    def test_update_statistics(self):
        visitor_ip = '127.0.0.1'
        day, month, year = self.collector.update_statistics(visitor_ip)

        self.assertEqual(len(self.collector.unique_visitors), 1)
        self.assertEqual(len(self.collector.unique_visits_by_day[day]), 1)
        self.assertEqual(len(self.collector.unique_visits_by_month[month]), 1)
        self.assertEqual(len(self.collector.unique_visits_by_year[year]), 1)
        self.assertEqual(self.collector.visits_by_day[day], 1)
        self.assertEqual(self.collector.visits_by_month[month], 1)
        self.assertEqual(self.collector.visits_by_year[year], 1)

    def test_init_with_existing_file(self, mock_load, mock_dump):
        collector = StatisticsCollector(self.dirty_file, self.clean_file)

        self.assertEqual(collector.visitors_count, 1)
        self.assertEqual(collector.unique_visitors, {'127.0.0.1'})

    def test_save_clean_statistics(self):
        self.collector.visitors_count = 5
        self.collector.unique_visitors = {'127.0.0.1', '192.168.0.1'}
        self.collector.visits_by_day = {'2023-01-01': 2, '2023-01-02': 3}
        self.collector.unique_visits_by_day = {
            '2023-01-01': {'127.0.0.1', '192.168.0.1'},
            '2023-01-02': {'127.0.0.1'}}

        # Вызываем сохранение статистики
        self.collector.save_clean_statistics()

        with open(self.clean_file, 'r') as f:
            clean_stats = json.load(f)

        self.assertEqual(clean_stats['total_visits'], 5)
        self.assertEqual(clean_stats['total_unique_visits'], 2)
        self.assertEqual(clean_stats['visits_by_day'],
                         {'2023-01-01': 2, '2023-01-02': 3})
        self.assertEqual(clean_stats['unique_visits_by_day'],
                         {'2023-01-01': 2, '2023-01-02': 1})


if __name__ == '__main__':
    unittest.main()
