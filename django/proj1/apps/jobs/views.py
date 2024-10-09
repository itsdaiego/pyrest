from rest_framework.decorators import api_view
from rest_framework.views import Response


@api_view(['POST'])
def create_job(request):
    return Response({'message': 'Job created successfully'}, status=201)

