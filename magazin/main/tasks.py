from celery import shared_task
from datetime import date
from .models import Subscription


@shared_task
def check_and_update_subscription_status():
    subscriptions = Subscription.objects.filter(status='Active')
    for subscription in subscriptions:
        if subscription.end_date and subscription.end_date < date.today():
            subscription.status = 'Expired'
            subscription.save()