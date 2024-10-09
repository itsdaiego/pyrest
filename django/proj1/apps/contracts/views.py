from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status

from proj1.apps.contracts.serializers import ContractSerializer


@api_view(['POST'])
def create_contract(request):
    serialize = ContractSerializer(data=request.data)

    if serialize.is_valid():
        serialize.save()

        return Response({
            "message": "Contract created successfully",
            "contract": serialize.data,
        } ,status=status.HTTP_201_CREATED)
