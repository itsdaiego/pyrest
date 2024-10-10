from django.views.generic.base import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status

from pyrest.apps.contracts.serializers import ContractSerializer


@api_view(['POST'])
def create_contract(request):
    try:
        serialize = ContractSerializer(data=request.data)

        if serialize.is_valid():
            serialize.save()
        else:
            logger.error("Contract serialization error:", serialize.errors)

            return Response({
                "message": "Contract creation failed",
                "error": serialize.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Contract created successfully",
            "contract": serialize.data,
        } ,status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(e)

        return Response({
            "message": "Contract creation failed",
            "error": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
