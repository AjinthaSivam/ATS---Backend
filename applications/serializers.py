from rest_framework import serializers
from .models import Application

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'resume', 'cover_letter']

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title')
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'full_name', 'email', 'phone', 'job_title', 'status', 'applied_at', 'resume_url', 'cover_letter']

    def get_resume_url(self, obj):
        if obj.resume:
            return obj.resume.url
        return None