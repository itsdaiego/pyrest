from rest_framework import serializers
from proj1.apps.contracts.models import Contract


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

        if client_id == contractor_id:
            raise serializers.ValidationError("Client and contractor cannot be the same.")

        return attrs

    
    def create(self, validated_data):
        return Contract.objects.create(**validated_data)
