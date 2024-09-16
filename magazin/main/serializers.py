from rest_framework import serializers
from .models import Subscription, Purchase, Review, Course, CourseAnalytics, UserProfile
from django.contrib.auth.models import User


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    course = serializers.ReadOnlyField(source='course.name')
    plan = serializers.ReadOnlyField(source='plan.plan_types')

    class Meta:
        model = Subscription
        fields = ['id', 'status', 'user', 'course', 'plan', 'price', 'start_date', 'end_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'course', 'purchase_date', 'is_paid']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    course = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Review
        fields = ['course', 'user', 'rating', 'comment', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True, source='avg_rating')

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'duration', 'full_price', 'average_rating']


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAnalytics
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subscriptions = SubscriptionSerializer(many=True, read_only=True, source='user.subscription')
    reviews = ReviewSerializer(many=True, read_only=True, source='user.review')
    purchases = PurchaseSerializer(many=True, read_only=True, source='user.purchase')
    completed_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'completed_courses', 'subscriptions', 'reviews', 'purchases']

    def get_user(self, obj):
        return obj.user.username




