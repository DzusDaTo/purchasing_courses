from rest_framework import serializers
from .models import Subscription, Purchase, Review, Course, CourseAnalytics
from django.contrib.auth.models import User


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


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
    class Meta:
        model = Review
        fields = ['course', 'rating', 'comment', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True, source='avg_rating')

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'duration', 'full_price', 'average_rating']


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAnalytics
        fields = '__all__'
