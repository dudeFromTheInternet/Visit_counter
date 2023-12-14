import json
import os
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch
from statistics_collector import StatisticsCollector


class TestStatisticsCollector(unittest.TestCase):
    def setUp(self):
        self.dirty_file = 'dirty_statistics.json'
        self.clean_file = 'clean_statistics.json'

    def tearDown(self):
        try:
            os.remove(self.dirty_file)
            os.remove(self.clean_file)
        except FileNotFoundError:
            pass

    def test_update_statistics(self):
        collector = StatisticsCollector(self.dirty_file, self.clean_file)
        visitor_ip = '127.0.0.1'

        day, month, year = collector.update_statistics(visitor_ip)

        self.assertIn(visitor_ip, collector.unique_visitors)
        self.assertIn(visitor_ip, collector.unique_visits_by_day[day])
        self.assertIn(visitor_ip, collector.unique_visits_by_month[month])
        self.assertIn(visitor_ip, collector.unique_visits_by_year[year])
        self.assertIn(visitor_ip, collector.unique_visits_by_hour[
            f'{year}-{month}-{day} {datetime.now().strftime("%H")}'])

        self.assertEqual(collector.visits_by_day[day], 1)
        self.assertEqual(collector.visits_by_month[month], 1)
        self.assertEqual(collector.visits_by_year[year], 1)
        self.assertEqual(collector.visits_by_hour[
                             f'{year}-{month}-{day} {datetime.now().strftime("%H")}'],
                         1)

        self.assertTrue(os.path.exists(self.dirty_file))
        self.assertTrue(os.path.exists(self.clean_file))

    @patch("builtins.open", new_callable=mock_open,
           read_data='{"total_visits": 10}')
    def test_load_from_file(self, mock_file_open):
        collector = StatisticsCollector(self.dirty_file, self.clean_file)

        self.assertEqual(collector.visitors_count, 10)

    def test_save_clean_statistics(self):
        collector = StatisticsCollector(self.dirty_file, self.clean_file)
        collector.visitors_count = 5
        collector.save_clean_statistics()

        with open(self.clean_file, 'r') as f:
            clean_stats = json.load(f)

        self.assertEqual(clean_stats['total_visits'], 5)

    def test_save_dirty_statistics(self):
        collector = StatisticsCollector(self.dirty_file, self.clean_file)
        collector.visitors_count = 8
        collector.save_dirty_statistics()

        with open(self.dirty_file, 'r') as f:
            dirty_stats = json.load(f)

        self.assertEqual(dirty_stats['total_visits'], 8)


if __name__ == '__main__':
    unittest.main()
