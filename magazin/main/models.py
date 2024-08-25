from datetime import timezone, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса')
    description = models.TextField(max_length=150, verbose_name='Описание курса')
    full_price = models.PositiveIntegerField(verbose_name='Полная стоимость')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность курса')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for subscrip in self.subscription.all():
            subscrip.save()

    def __str__(self):
        return f"Курсы: {self.name, self.full_price}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} приобрел {self.course.name} оплата {self.is_paid}"


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'FULL'),
        ('student', 'STUDENT'),
        ('discount', 'DISCOUNT')
    )

    plan_types = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(100)
    ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for subscrip in self.subscription.all():
            subscrip.save()

    def __str__(self):
        return f"План: {self.plan_types,self.discount_percent}"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    user = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='subscription', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name='subscription', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.course and self.plan:
            full_price = self.course.full_price
            discount = self.plan.discount_percent
            self.price = full_price - (full_price * discount / 100)

        if not self.end_date:
            if self.course and self.course.duration:
                self.end_date = self.start_date + timedelta(days=self.course.duration)
            else:
                print("Course duration not set or course not found")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Подписки: {self.user,self.course,self.price,self.plan,self.end_date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    completed_courses = models.ManyToManyField(Course, related_name='completed_course')

    def __str__(self):
        return f"Профиль: {self.user}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name} ({self.rating})'