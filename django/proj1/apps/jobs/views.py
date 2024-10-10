from django.views.generic.base import logger
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from proj1.apps.jobs.models import Job
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


@api_view(['POST'])
def perform_payment(request, job_id):
    try:
        serializer = JobSerializer(data=request.data)
    except Exception as e:
        return Response({
            "message": "An error occurred while initializing the serializer",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        job = get_object_or_404(Job, id=job_id)
        paid_job = serializer.perform_payment(job)

        return Response({
            "message": "Job paid successfully",
            "job": JobSerializer(paid_job).data,
        }, status=status.HTTP_200_OK)

    except serializers.ValidationError as e:
        return Response({
            "message": "Payment failed",
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error('An error occurred while paying the job: %s', str(e))

        return Response({
            "message": "An error occurred while paying the job",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

