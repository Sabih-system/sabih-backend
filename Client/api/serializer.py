from rest_framework import serializers
from Client.models import UsersideRequest


class UsersideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersideRequest
        fields = '__all__'
