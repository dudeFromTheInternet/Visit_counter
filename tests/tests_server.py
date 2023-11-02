import json
import unittest
from server import (update_statistics, save_clean_statistics,
                    save_dirty_statistics)


class TestVisitorCounter(unittest.TestCase):
    def test_update_statistics(self):
        initial_visitors_count = visitors_count
        initial_unique_visitors = len(unique_visitors)
        initial_visits_by_day = dict(visits_by_day)

        day, month, year = update_statistics(self.visitor_ip)

        self.assertEqual(visitors_count, initial_visitors_count + 1)
        self.assertEqual(len(unique_visitors), initial_unique_visitors + 1)
        self.assertEqual(visits_by_day[day],
                         initial_visits_by_day.get(day, 0) + 1)


    def test_save_clean_statistics(self):
        # Предполагается, что функция сохранения данных работает корректно
        global visitors_count, unique_visitors, visits_by_day, \
            unique_visits_by_day, visits_by_month, unique_visits_by_month, \
            visits_by_year, unique_visits_by_year

        visitors_count = 10
        unique_visitors = {'192.168.0.1', '192.168.0.2'}
        visits_by_day = {'2023-11-01': 10, '2023-11-02': 20}
        unique_visits_by_day = {'2023-11-01': {'192.168.0.1', '192.168.0.2'},
                                '2023-11-02': {'192.168.0.1'}}

        save_clean_statistics()

        with open('statistics/clean_statistics.json', 'r') as f:
            clean_stats = json.load(f)

        self.assertEqual(clean_stats['total_visits'], visitors_count)
        self.assertEqual(len(clean_stats['total_unique_visits']),
                         len(unique_visitors))
        self.assertEqual(clean_stats['visits_by_day'], visits_by_day)
        self.assertEqual(clean_stats['unique_visits_by_day'], {k: len(v) for k,
        v in unique_visits_by_day.items()})

    def test_save_dirty_statistics(self):
        visitors_count = 10
        unique_visitors = {'192.168.0.1', '192.168.0.2'}
        visits_by_day = {'2023-11-01': 10, '2023-11-02': 20}
        unique_visits_by_day = {'2023-11-01': {'192.168.0.1', '192.168.0.2'},
                                '2023-11-02': {'192.168.0.1'}}

        save_dirty_statistics()  # Сохраняем "чистую" статистику

        with open('statistics/dirty_statistics.json', 'r') as f:
            clean_stats = json.load(f)

        self.assertEqual(clean_stats['total_visits'], visitors_count)
        self.assertEqual(len(clean_stats['total_unique_visits']),
                         len(unique_visitors))
        self.assertEqual(clean_stats['visits_by_day'], visits_by_day)
        self.assertEqual(clean_stats['unique_visits_by_day'],
                         {k: len(v) for k, v in unique_visits_by_day.items()})


if __name__ == '__main__':
    unittest.main()
