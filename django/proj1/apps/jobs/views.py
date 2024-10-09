from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import Response

from proj1.apps.jobs.serializers import JobSerializer


@api_view(['POST'])
def create_job(request):
    serializer = JobSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        Response({
            "message": "Job created successfully",
            "job": serializer.data,
        }, status=status.HTTP_201_CREATED)

