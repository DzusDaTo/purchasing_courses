from django.db.models import Avg
from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Subscription, Purchase, Review, Course, CourseAnalytics
from .serializers import SubscriptionSerializer, RegisterSerializer, PurchaseSerializer, ReviewSerializer, \
    CourseSerializer, CourseAnalyticsSerializer, UserProfileSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related('user', 'course', 'plan').only(
        'id', 'status', 'user__username', 'course__name', 'plan__plan_types',
        'price', 'start_date', 'end_date'
    )
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
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Просмотр и создание отзыва и присваивание отзыва пользователю
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.select_related('course', 'user').only(
        'user__username', 'course__name', 'rating', 'comment', 'created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Просмотр отзывов, оставленных самим пользователем
class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('course')


# Просмотр всех курсов
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.annotate(avg_rating=Avg('review__rating')).all()
    serializer_class = CourseSerializer


# Аналитика
class CourseAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseAnalytics.objects.select_related('course').all()
    serializer_class = CourseAnalyticsSerializer


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем объект профиля пользователя, который связан с текущим аутентифицированным пользователем
        return self.request.user.userprofile
