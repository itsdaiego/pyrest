from rest_framework import serializers
from proj1.apps import job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = job
        fields = '__all__'
