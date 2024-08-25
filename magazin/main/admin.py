from django.contrib import admin
from .models import Course, Plan, Subscription, UserProfile, Purchase

admin.site.register(Course)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(UserProfile)
admin.site.register(Purchase)
