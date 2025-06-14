from rest_framework import serializers
from ..models import Project, Client


class ProjectProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'fname', 'lname', 'phone', 'email', 'company',
            'project_type', 'budget', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Access request context
        user = self.context['request'].user if 'request' in self.context else None

        # If user is already a client, make personal fields not required
        if hasattr(user, 'client'):
            for field in ['fname', 'lname', 'phone', 'email', 'company']:
                self.fields[field].required = False

    def validate(self, attrs):
        user = self.context['request'].user

        if not hasattr(user, 'client'):
            # Ensure all personal fields are provided for first-time proposal
            required_fields = ['fname', 'lname', 'phone', 'email', 'company']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError({field: "This field is required."})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None) 

        if hasattr(user, 'client'):
            client = user.client
            validated_data.update({
                'fname': client.fname,
                'lname': client.lname,
                'phone': client.phone,
                'email': client.email,
                'company': client.company,
            })
        else:
            client = None

        project = Project.objects.create(
            user=user,
            client=client,
            **validated_data
        )
        return project




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['user']

