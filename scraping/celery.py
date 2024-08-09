from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping.settings')
import django
django.setup()

app = Celery('scraping')



app.config_from_object('django.conf:settings',
                       namespace='CELERY')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

broker_connection_retry_on_startup = True




# Load task modules from all registered Django app configs.
app.autodiscover_tasks()