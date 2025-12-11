from rest_framework import serializers
from .models import Job

class JobListSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'salary', 'description', 'requirements', 'applications_count']

    def get_applications_count(self, obj):
        return obj.applications.count()

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'