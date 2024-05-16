from rest_framework import serializers
from .models import Course, Review

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'slug', 'title', 'summary','teacher','level', 'file', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'student', 'rating', 'comment', 'created_at']
