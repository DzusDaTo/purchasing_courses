from celery import shared_task
from datetime import date

from django.db.models import Avg, Sum

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
    print("Updating course analytics...")
    for course in Course.objects.all():
        # Вычисляем средний рейтинг
        average_rating = course.review.aggregate(Avg('rating'))['rating__avg'] or 0

        # Количество подписок (подписчиков)
        subscriber_count = course.subscription.count()

        # Доход от курса
        total_income = course.subscription.filter(status='Active').aggregate(Sum('price'))['price__sum'] or 0

        # Обновляем или создаем запись аналитики
        analytics, created = CourseAnalytics.objects.get_or_create(course=course)
        analytics.average_rating = average_rating
        analytics.subscriber_count = subscriber_count
        analytics.total_income = total_income
        analytics.save()
