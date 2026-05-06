"""Celery app for distributed crawling tasks."""
from celery import Celery
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

app = Celery('crawler', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)


@app.task(bind=True, max_retries=3)
def crawl_url(self, url, depth=0, max_depth=3):
    """Celery task to crawl a single URL."""
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'lxml')
        
        data = {
            'url': url,
            'status_code': response.status_code,
            'title': soup.title.string if soup.title else None,
            'depth': depth
        }
        
        links = []
        if depth < max_depth:
            links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        return {'data': data, 'links': links}
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
        raise self.retry(exc=e, countdown=60)
