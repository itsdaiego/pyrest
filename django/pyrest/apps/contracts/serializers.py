from rest_framework import serializers
from pyrest.apps.contracts.models import Contract
from pyrest.apps.profiles.models import Profile


class ContractSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(required=True)
    contractor_id = serializers.IntegerField(required=True)

    class Meta:
        model = Contract
        fields = (
            'id',
            'client_id',
            'contractor_id',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


    def validate(self, attrs):
        client_id = attrs.get('client_id')
        contractor_id = attrs.get('contractor_id')

        client = Profile.objects.filter(id=client_id).first()

        if not client:
            raise serializers.ValidationError("Client not found.")

        contractor = Profile.objects.filter(id=contractor_id).first()

        if not contractor:
            raise serializers.ValidationError("Contractor not found.")

        if client_id == contractor_id:
            raise serializers.ValidationError("Client and contractor cannot be the same.")

        return attrs

    
    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
