from rest_framework import serializers
from ..models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['timestamp', 'is_read']

    def validate(self, data):
        content = data.get("content", "")
        file = data.get("file", None)

        if not content and not file:
            raise serializers.ValidationError("Message must have text content or a file.")
        return data
