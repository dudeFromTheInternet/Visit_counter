import json
from datetime import datetime, timedelta
from collections import defaultdict
import calendar


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
        self.visits_by_hour = defaultdict(int)
        self.unique_visits_by_hour = defaultdict(set)

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
                self.visits_by_hour = dict(data.get('visits_by_hour', {}))
                self.unique_visits_by_hour = dict({k: set(v) for k, v in
                                                   data.get(
                                                       'unique_visits_by_hour',
                                                       {}).items()})
        except FileNotFoundError:
            pass

    def update_statistics(self, visitor_ip):
        now = datetime.now()
        day = now.strftime('%Y-%m-%d')
        month = now.strftime('%Y-%m')
        year = now.strftime('%Y')
        hour = now.strftime('%Y-%m-%d %H')

        self.unique_visitors.add(visitor_ip)

        if day not in self.unique_visits_by_day.keys():
            self.unique_visits_by_day[day] = set()
        if month not in self.unique_visits_by_month.keys():
            self.unique_visits_by_month[month] = set()
        if year not in self.unique_visits_by_year.keys():
            self.unique_visits_by_year[year] = set()
        if hour not in self.unique_visits_by_hour.keys():
            self.unique_visits_by_hour[hour] = set()
        self.unique_visits_by_day[day].add(visitor_ip)
        self.unique_visits_by_month[month].add(visitor_ip)
        self.unique_visits_by_year[year].add(visitor_ip)
        self.unique_visits_by_hour[hour].add(visitor_ip)

        if day not in self.visits_by_day.keys():
            self.visits_by_day[day] = 0
        if month not in self.visits_by_month.keys():
            self.visits_by_month[month] = 0
        if year not in self.visits_by_year.keys():
            self.visits_by_year[year] = 0
        if hour not in self.visits_by_hour.keys():
            self.visits_by_hour[hour] = 0
        self.visits_by_day[day] += 1
        self.visits_by_month[month] += 1
        self.visits_by_year[year] += 1
        self.visits_by_hour[hour] += 1

        self.save_dirty_statistics()
        self.save_clean_statistics()

        return day, month, year

    def get_hourly_statistics(self, day):
        hourly_stats = defaultdict(str)
        unique_hourly_stats = defaultdict(int)

        for hour in self.visits_by_hour:
            if hour.startswith(day):
                formatted_time = datetime.strptime(hour,
                                                   '%Y-%m-%d %H').strftime(
                    '%H:%M')
                hourly_stats[formatted_time] = self.visits_by_hour[hour]
                unique_hourly_stats[formatted_time] = len(
                    self.unique_visits_by_hour.get(hour, []))

        if hourly_stats:
            result = f"Hourly Statistics for {day}:\n"
            for hour in hourly_stats:
                result += (f"{hour}: Total Visits:"
                           f" {hourly_stats[hour]}, "
                           f"Unique Visits: {unique_hourly_stats[hour]}\n")
            return result
        else:
            return f"No hourly statistics available for {day}"

    def get_daily_statistics(self, day):
        if day in self.visits_by_day:
            return (f"Statistics for {day}:\nTotal Visits: "
                    f"{self.visits_by_day[day]}\nUnique Visits: "
                    f"{len(self.unique_visits_by_day.get(day, []))}")
        else:
            return f"No statistics available for {day}"

    def get_month_statistics(self, month):
        if month in self.visits_by_month:
            return (f"Statistics for {month}:\nTotal Visits: "
                    f"{self.visits_by_month[month]}\nUnique Visits: "
                    f"{len(self.unique_visits_by_month.get(month, []))}")
        else:
            return f"No statistics available for {month}"

    def get_hourly_statistics_range(self, start_day, end_day):
        hourly_stats_range = defaultdict(str)
        unique_hourly_stats_range = defaultdict(int)

        current_day = datetime.strptime(start_day, '%Y-%m-%d')
        end_date = datetime.strptime(end_day, '%Y-%m-%d')

        while current_day <= end_date:
            current_day_str = current_day.strftime('%Y-%m-%d')
            for hour in self.visits_by_hour:
                if hour.startswith(current_day_str):
                    formatted_time = datetime.strptime(hour,
                                                       '%Y-%m-%d %H').strftime(
                        '%H:%M')
                    hourly_stats_range[(current_day_str, formatted_time)] = \
                        self.visits_by_hour[hour]
                    unique_hourly_stats_range[
                        (current_day_str, formatted_time)] = len(
                        self.unique_visits_by_hour.get(hour, []))

            current_day += timedelta(days=1)

        if hourly_stats_range:
            result = "Hourly Statistics Range:\n"
            for (day, hour) in hourly_stats_range:
                result += (f"{day} {hour}: Total Visits:"
                           f" {hourly_stats_range[(day, hour)]}, "
                           f"Unique Visits: {unique_hourly_stats_range[(day, hour)]}\n")
            return result
        else:
            return f"No hourly statistics available for the specified range"

    def get_daily_statistics_in_month(self, month):
        daily_stats_in_month = defaultdict(str)

        # Convert month string to datetime object
        month_start = datetime.strptime(month, '%Y-%m')

        for day in range(1, 32):
            current_day_str = f'{month}-{day:02d}'
            current_day = datetime.strptime(current_day_str, '%Y-%m-%d')

            if current_day <= month_start + timedelta(days=calendar.monthrange(
                    month_start.year, month_start.month)[1] - 1):
                if current_day_str in self.visits_by_day:
                    daily_stats_in_month[current_day_str] = (
                        f"Statistics for {current_day_str}:\nTotal Visits: "
                        f"{self.visits_by_day[current_day_str]}\nUnique Visits: "
                        f"{len(self.unique_visits_by_day.get(current_day_str, []))}")

        if daily_stats_in_month:
            result = "Daily Statistics in {}:\n".format(month)
            for day, stats in daily_stats_in_month.items():
                result += f"{stats}\n"
        else:
            result = f"No daily statistics available for {month}"

        return result

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
                                      self.unique_visits_by_year.items()},
            'visits_by_hour': dict(self.visits_by_hour),
            'unique_visits_by_hour': {k: len(v) for k, v in
                                      self.unique_visits_by_hour.items()}
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
                                      self.unique_visits_by_year.items()},
            'visits_by_hour': dict(self.visits_by_hour),
            'unique_visits_by_hour': {k: list(v) for k, v in
                                      self.unique_visits_by_hour.items()}
        }
        with open(self.dirty_file, 'w') as f:
            json.dump(dirty_stats, f)
