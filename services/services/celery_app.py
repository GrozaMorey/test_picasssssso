from __future__ import absolute_import, unicode_literals
import os
import time

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

app = Celery('services')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

@app.task()
def debug_task():
    time.sleep(20)
    print("zopich")
