from rest_framework import serializers
from proj1.apps.jobs.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'description',
            'price',
            'paid',
            'payment_date',
            'contract_id'
        )

    def create(self, validated_data):
        return Job.objects.create(**validated_data)
