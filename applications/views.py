from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationCreateSerializer, ApplicationSerializer
from jobs.models import Job

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().select_related('job')
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def submit(self, request):
        job_id = request.data.get('job_id')
        try:
            job = Job.objects.get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

        serializer = ApplicationCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(job=job)
            return Response({"message": "Application submitted successfully!"}, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        app = self.get_object()
        status_val = request.data.get('status')
        if status_val in dict(Application.STATUS_CHOICES):
            app.status = status_val
            app.save()
            return Response({"status": "updated"})
        return Response({"error": "Invalid status"}, status=400)