import json
from django.db.models.query_utils import logging
from django.http import JsonResponse
from .models import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer

@api_view(['GET'])
def get(request):
    try:
        profiles = Profile.objects.all().values('id', 'first_name', 'last_name', 'profession', 'type')
        request.COOKIES.get('csrftoken')

        return JsonResponse(list(profiles), safe=False)
    except Exception as e:
        logging.error(str(e))
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def post(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


