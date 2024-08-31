from celery import shared_task
from datetime import date

from django.db.models import Avg, Count, Sum, Q

from .models import Subscription, Course, CourseAnalytics


@shared_task
def check_and_update_subscription_status():
    print("Updating subscription status...")
    subscriptions = Subscription.objects.filter(status='Active')
    for subscription in subscriptions:
        if subscription.end_date and subscription.end_date < date.today():
            subscription.status = 'Expired'
            subscription.save()


@shared_task
def update_course_analytics():
    analytics_data = Course.objects.annotate(
        avg_course_rating=Avg('review__rating'),  # Измененное имя аннотации для среднего рейтинга
        subscriber_count=Count('subscription'),
        total_income=Sum('subscription__price', filter=Q(subscription__status='Active')),
        completed_courses=Count('subscription', filter=Q(subscription__status='Completed'))
    ).values('id', 'avg_course_rating', 'subscriber_count', 'total_income', 'completed_courses')

    for data in analytics_data:
        CourseAnalytics.objects.update_or_create(
            course_id=data['id'],
            defaults={
                'average_rating': data['avg_course_rating'] or 0,  # Применение нового имени аннотации
                'subscriber_count': data['subscriber_count'] or 0,
                'total_income': data['total_income'] or 0,
                'completed_courses': data['completed_courses'] or 0,
            }
        )

