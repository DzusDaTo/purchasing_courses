from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, RegisterView, PurchaseCourseView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('purchase/', PurchaseCourseView.as_view(), name='purchase-course'),
]
