from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, CourseAnalyticsViewSet, \
    RegisterView, PurchaseCourseView, ReviewListCreateView, UserReviewListView, CourseListView

router = DefaultRouter()

router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'course-analytics', CourseAnalyticsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/purchase/', PurchaseCourseView.as_view(), name='purchase-course'),
    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('api/my-reviews/', UserReviewListView.as_view(), name='user-reviews'),
    path('api/courses/', CourseListView.as_view(), name='course-list'),
]

