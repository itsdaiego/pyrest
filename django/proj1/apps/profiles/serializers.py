from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, min_length=2, required=True)
    last_name = serializers.CharField(max_length=100, min_length=2, required=True)
    profession = serializers.CharField(max_length=100, min_length=8, required=True)
    type = serializers.ChoiceField(choices=[('client', 'Client'), ('contractor', 'Contractor')], required=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'profession', 'type', 'user_id', 'balance', 'created_at', 'updated_at')
        read_only_fields = ('id', 'balance', 'created_at', 'updated_at')

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)

        return profile
