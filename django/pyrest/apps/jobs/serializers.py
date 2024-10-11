from django.core.handlers.base import logger
from rest_framework import serializers
from pyrest.apps.contracts.models import Contract
from pyrest.apps.jobs.models import Job
from django.utils import timezone
from django.db import transaction


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

        try:
            with transaction.atomic():
                # Lock the rows we're going to update
                job = Job.objects.select_for_update().get(pk=job.pk)
                client = job.contract.client.__class__.objects.select_for_update().get(pk=job.contract.client.pk)
                contractor = job.contract.contractor.__class__.objects.select_for_update().get(pk=job.contract.contractor.pk)

                if client.balance < job.price:
                    raise serializers.ValidationError('Insufficient funds')

                client.balance -= job.price
                contractor.balance += job.price
                job.paid = True
                job.payment_date = timezone.now()

                client.save()
                contractor.save()
                job.save()

        except Exception as e:
            logger.error('An error occurred while performing the payment: %s', str(e))
            raise serializers.ValidationError(f'Transaction failed: {str(e)}')

        return job
