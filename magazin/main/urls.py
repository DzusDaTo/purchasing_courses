from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, RegisterView, PurchaseCourseView, ReviewListCreateView, UserReviewListView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('purchase/', PurchaseCourseView.as_view(), name='purchase-course'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('my-reviews/', UserReviewListView.as_view(), name='user-reviews'),
]
