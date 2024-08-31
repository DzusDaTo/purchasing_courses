import os
import time
from datetime import timedelta

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin.settings')

app = Celery('magazin')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-subscriptions-daily': {
        'task': 'main.tasks.check_and_update_subscription_status',
        'schedule': crontab(hour=0, minute=0),  # ежедневно в полночь
    },
    'update-course-analytics-every-minute': {
        'task': 'main.tasks.update_course_analytics',
        'schedule': timedelta(minutes=1),
    },
}
