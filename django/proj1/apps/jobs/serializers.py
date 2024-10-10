from rest_framework import serializers
from proj1.apps.contracts.models import Contract
from proj1.apps.jobs.models import Job
from django.utils import timezone


class JobSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    paid = serializers.BooleanField()
    payment_date = serializers.DateTimeField()
    contract_id = serializers.IntegerField()

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

    def validate(self, attrs):
        contract = Contract.objects.filter(id=attrs['contract_id']).first()

        if not contract:
            raise serializers.ValidationError('Contract does not exist')

        return attrs

    def create(self, validated_data):
        return Job.objects.create(**validated_data)


    def perform_payment(self, job):
        if job.paid:
            raise serializers.ValidationError('This job has already been paid')

        client = job.contract.client
        contractor = job.contract.contractor

        if client.balance < job.price:
            raise serializers.ValidationError('Insufficient funds')

        client.balance -= job.price
        contractor.balance += job.price
        job.paid = True
        job.payment_date = timezone.now()

        client.save()
        contractor.save()
        job.save()

        return job
