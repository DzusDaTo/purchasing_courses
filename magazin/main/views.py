from django.db.models import Avg, Count, Sum
from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Subscription, Purchase, Review, Course, CourseAnalytics
from .serializers import SubscriptionSerializer, RegisterSerializer, PurchaseSerializer, ReviewSerializer, \
    CourseSerializer, CourseAnalyticsSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    # Подгрузка данных одним запрос
    queryset = Subscription.objects.select_related('user', 'course', 'plan').all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'user': RegisterSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token,
        })


class PurchaseCourseView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Просмотр и создание отзыва и присваивание отзыва пользователю
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Просмотр отзывов, оставленных самим пользователем
class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


# Просмотр всех курсов
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Аналитика
class CourseAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseAnalytics.objects.select_related('course')
    serializer_class = CourseAnalyticsSerializer


