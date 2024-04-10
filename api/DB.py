import datetime
from django.core.management.base import BaseCommand
from .models import News
import requests
import logging
from django.conf import settings

class DataManager(BaseCommand):
    help = 'Fetch news from API and update database'
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=f'{settings.BASE_DIR}/DB.log', level=logging.INFO)

    def handleData(self, url):
        response = requests.get(url ,headers={"Authorization": "f332b807d748498798b3c440e20a84ed"})
        data = response.json()

        for item in data['articles']:
            News.objects.update_or_create(
                url=item['url'],
                defaults={
                    'url': item["url"],
                    'title': item['title'],
                    'description': item['description'],
                    'content': item['content'],
                    'publishedAt': item['publishedAt'],
                    'source': item['source']['name'],
                    'author': item['author']
                }
            )

    def sync(self):
        url = f'https://newsapi.org/v2/everything?q=i'
        self.handleData(url)
        self.logger.info(f'Data initialization at {datetime.datetime.now()}')

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        url = f'https://newsapi.org/v2/everything?q=i&from={now.year}-{now.month}-{now.day}T{now.hour-1}'
        self.handleData(url)
        self.logger.info(f'Periodic data sync at {datetime.datetime.now()}')