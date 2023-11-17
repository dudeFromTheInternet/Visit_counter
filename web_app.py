from aiohttp import web
from statistics_collector import StatisticsCollector


class WebApp:
    def __init__(self, collector):
        self.app = web.Application()
        self.collector = collector

    async def handle(self, request):
        self.collector.visitors_count += 1
        visitor_ip = request.remote
        day, month, year = self.collector.update_statistics(visitor_ip)

        with open('page.html', 'r') as f:
            html_content = f.read()

        html_content = html_content.replace('<!--total_visits-->',
                                            str(self.collector.visitors_count))
        html_content = html_content.replace('<!--total_unique_visits-->',
                                            str(len(
                                                self.collector.unique_visitors)))

        html_content = html_content.replace('<!--visits_by_day-->',
                                            f'<li>{day}: {self.collector.visits_by_day[day]}</li>')
        html_content = html_content.replace('<!--unique_visits_by_day-->',
                                            f'<li>{day}: {len(self.collector.unique_visits_by_day[day])}</li>')

        html_content = html_content.replace('<!--visits_by_month-->',
                                            f'<li>{month}: {self.collector.visits_by_month[month]}</li>')
        html_content = html_content.replace('<!--unique_visits_by_month-->',
                                            f'<li>{month}: {len(self.collector.unique_visits_by_month[month])}</li>')

        html_content = html_content.replace('<!--visits_by_year-->',
                                            f'<li>{year}: {self.collector.visits_by_year[year]}</li>')
        html_content = html_content.replace('<!--unique_visits_by_year-->',
                                            f'<li>{year}: {len(self.collector.unique_visits_by_year[year])}</li>')

        return web.Response(text=html_content, content_type='text/html')

    async def get_statistics(self):
        with open(self.collector.clean_file, 'r') as f:
            return web.Response(text=f.read())

    def run(self):
        self.app.router.add_get('/', self.handle)
        self.app.router.add_get('/statistics', self.get_statistics)
        web.run_app(self.app, host='localhost', port=8080)


if __name__ == '__main__':
    collector = StatisticsCollector('statistics/dirty_statistics.json',
                                    'statistics/clean_statistics.json')
    web_app = WebApp(collector)
    web_app.run()
