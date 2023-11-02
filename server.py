from collections import defaultdict
from aiohttp import web
import json
from datetime import datetime

app = web.Application()

visitors_count = 0
unique_visitors = set()
visits_by_day = defaultdict(int)
unique_visits_by_day = defaultdict(set)
visits_by_month = defaultdict(int)
unique_visits_by_month = defaultdict(set)
visits_by_year = defaultdict(int)
unique_visits_by_year = defaultdict(set)

clean_statistics_file = 'clean_statistics.json'
dirty_statistics_file = 'dirty_statistics.json'

try:
    with open(dirty_statistics_file, 'r') as f:
        data = json.load(f)
        visitors_count = data.get('total_visits', 0)
        unique_visitors = set(data.get('total_unique_visits', []))
        visits_by_day = dict(data.get('visits_by_day', {}))
        unique_visits_by_day = dict({k: set(v) for k, v in data.get(
            'unique_visits_by_day',
            {}).items()})
        visits_by_month = dict(data.get('visits_by_month', {}))
        unique_visits_by_month = dict({k: set(v) for k, v in data.get(
            'unique_visits_by_month',
            {}).items()})
        visits_by_year = dict(data.get('visits_by_year', {}))
        unique_visits_by_year = dict({k: set(v) for k, v in data.get(
            'unique_visits_by_year',
            {}).items()})
except FileNotFoundError:
    pass


async def handle(request):
    global visitors_count, unique_visitors, visits_by_day, \
        unique_visits_by_day, visits_by_month, unique_visits_by_month, \
        visits_by_year, unique_visits_by_year

    visitors_count += 1
    visitor_ip = request.remote

    now = datetime.now()
    day = now.strftime('%Y-%m-%d')
    month = now.strftime('%Y-%m')
    year = now.strftime('%Y')

    unique_visitors.add(visitor_ip)

    unique_visits_by_day[day].add(visitor_ip)
    unique_visits_by_month[month].add(visitor_ip)
    unique_visits_by_year[year].add(visitor_ip)

    visits_by_day[day] += 1
    visits_by_month[month] += 1
    visits_by_year[year] += 1

    save_dirty_statistics()
    save_clean_statistics()

    with open('page.html', 'r') as f:
        html_content = f.read()

    html_content = html_content.replace('<!--total_visits-->',
                                        str(visitors_count))
    html_content = html_content.replace('<!--total_unique_visits-->',
                                        str(len(unique_visitors)))

    html_content = html_content.replace('<!--visits_by_day-->',
                                        f'<li>{day}: '
                                        f'{visits_by_day[day]}</li>')
    html_content = html_content.replace('<!--unique_visits_by_day-->',
                                        f'<li>{day}: '
                                        f'{len(unique_visits_by_day[day])}'
                                        f'</li>')

    html_content = html_content.replace('<!--visits_by_month-->',
                                        f'<li>{month}: '
                                        f'{visits_by_month[month]}</li>')
    html_content = html_content.replace('<!--unique_visits_by_month-->',
                                        f'<li>{month}: '
                                        f'{len(unique_visits_by_month[month])}'
                                        f'</li>')

    html_content = html_content.replace('<!--visits_by_year-->',
                                        f'<li>{year}: '
                                        f'{visits_by_year[year]}</li>')
    html_content = html_content.replace('<!--unique_visits_by_year-->',
                                        f'<li>{year}: '
                                        f'{len(unique_visits_by_year[year])}'
                                        f'</li>')

    return web.Response(text=html_content, content_type='text/html')


async def get_statistics(request):
    with open(clean_statistics_file, 'r') as f:
        return web.Response(text=f.read())


def save_clean_statistics():
    clean_stats = {
        'total_visits': visitors_count,
        'total_unique_visits': len(unique_visitors),
        'visits_by_day': dict(visits_by_day),
        'unique_visits_by_day': {k: len(v) for k, v in
                                 unique_visits_by_day.items()},
        'visits_by_month': dict(visits_by_month),
        'unique_visits_by_month': {k: len(v) for k, v in
                                   unique_visits_by_month.items()},
        'visits_by_year': dict(visits_by_year),
        'unique_visits_by_year': {k: len(v) for k, v in
                                  unique_visits_by_year.items()}
    }
    with open(clean_statistics_file, 'w') as f:
        json.dump(clean_stats, f)


def save_dirty_statistics():
    dirty_stats = {
        'total_visits': visitors_count,
        'total_unique_visits': list(unique_visitors),
        'visits_by_day': dict(visits_by_day),
        'unique_visits_by_day': {k: list(v) for k, v in
                                 unique_visits_by_day.items()},
        'visits_by_month': dict(visits_by_month),
        'unique_visits_by_month': {k: list(v) for k, v in
                                   unique_visits_by_month.items()},
        'visits_by_year': dict(visits_by_year),
        'unique_visits_by_year': {k: list(v) for k, v in
                                  unique_visits_by_year.items()}
    }
    with open(dirty_statistics_file, 'w') as f:
        json.dump(dirty_stats, f)


app.router.add_get('/', handle)
app.router.add_get('/statistics', get_statistics)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8080)
