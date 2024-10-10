from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import Response

from proj1.apps.jobs.serializers import JobSerializer


@api_view(['POST'])
def create_job(request):
    try:
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Job created successfully",
                "job": serializer.data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "An error occurred while creating the job",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "message": "An error occurred while creating the job",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
