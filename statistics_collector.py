import json
from datetime import datetime
from collections import defaultdict


class StatisticsCollector:
    def __init__(self, dirty_file, clean_file):
        self.dirty_file = dirty_file
        self.clean_file = clean_file
        self.visitors_count = 0
        self.unique_visitors = set()
        self.visits_by_day = defaultdict(int)
        self.unique_visits_by_day = defaultdict(set)
        self.visits_by_month = defaultdict(int)
        self.unique_visits_by_month = defaultdict(set)
        self.visits_by_year = defaultdict(int)
        self.unique_visits_by_year = defaultdict(set)

        try:
            with open(self.dirty_file, 'r') as f:
                data = json.load(f)
                self.visitors_count = data.get('total_visits', 0)
                self.unique_visitors = set(data.get('total_unique_visits', []))
                self.visits_by_day = dict(data.get('visits_by_day', {}))
                self.unique_visits_by_day = dict({k: set(v) for k, v in
                                                  data.get(
                                                      'unique_visits_by_day',
                                                      {}).items()})
                self.visits_by_month = dict(data.get('visits_by_month', {}))
                self.unique_visits_by_month = dict({k: set(v) for k, v in
                                                    data.get(
                                                        'unique_visits_by_month',
                                                        {}).items()})
                self.visits_by_year = dict(data.get('visits_by_year', {}))
                self.unique_visits_by_year = dict({k: set(v) for k, v in
                                                   data.get(
                                                       'unique_visits_by_year',
                                                       {}).items()})
        except FileNotFoundError:
            pass

    def update_statistics(self, visitor_ip):
        now = datetime.now()
        day = now.strftime('%Y-%m-%d')
        month = now.strftime('%Y-%m')
        year = now.strftime('%Y')

        self.unique_visitors.add(visitor_ip)

        self.unique_visits_by_day[day].add(visitor_ip)
        self.unique_visits_by_month[month].add(visitor_ip)
        self.unique_visits_by_year[year].add(visitor_ip)

        self.visits_by_day[day] += 1
        self.visits_by_month[month] += 1
        self.visits_by_year[year] += 1

        self.save_dirty_statistics()
        self.save_clean_statistics()

        return day, month, year

    def save_clean_statistics(self):
        clean_stats = {
            'total_visits': self.visitors_count,
            'total_unique_visits': len(self.unique_visitors),
            'visits_by_day': dict(self.visits_by_day),
            'unique_visits_by_day': {k: len(v) for k, v in
                                     self.unique_visits_by_day.items()},
            'visits_by_month': dict(self.visits_by_month),
            'unique_visits_by_month': {k: len(v) for k, v in
                                       self.unique_visits_by_month.items()},
            'visits_by_year': dict(self.visits_by_year),
            'unique_visits_by_year': {k: len(v) for k, v in
                                      self.unique_visits_by_year.items()}
        }
        with open(self.clean_file, 'w') as f:
            json.dump(clean_stats, f)

    def save_dirty_statistics(self):
        dirty_stats = {
            'total_visits': self.visitors_count,
            'total_unique_visits': list(self.unique_visitors),
            'visits_by_day': dict(self.visits_by_day),
            'unique_visits_by_day': {k: list(v) for k, v in
                                     self.unique_visits_by_day.items()},
            'visits_by_month': dict(self.visits_by_month),
            'unique_visits_by_month': {k: list(v) for k, v in
                                       self.unique_visits_by_month.items()},
            'visits_by_year': dict(self.visits_by_year),
            'unique_visits_by_year': {k: list(v) for k, v in
                                      self.unique_visits_by_year.items()}
        }
        with open(self.dirty_file, 'w') as f:
            json.dump(dirty_stats, f)
