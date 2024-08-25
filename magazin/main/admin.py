from django.contrib import admin
from .models import Course, Plan, Subscription, UserProfile, Purchase, Review

admin.site.register(Course)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(UserProfile)
admin.site.register(Purchase)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    search_fields = ('user__username', 'course__name')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Review, ReviewAdmin)