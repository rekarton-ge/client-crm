from rest_framework import serializers
from .models import Client, ClientTag, ClientGroup


class ClientTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTag
        fields = ['id', 'name', 'color', 'description']


class ClientGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientGroup
        fields = ['id', 'name', 'description', 'is_dynamic', 'filter_criteria']


class ClientSerializer(serializers.ModelSerializer):
    tags = ClientTagSerializer(many=True, read_only=True)
    groups = ClientGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'whatsapp',
            'company', 'position', 'address', 'tags', 'status',
            'source', 'created_at', 'updated_at', 'last_contacted',
            'notes', 'groups'
        ]
        read_only_fields = ['created_at', 'updated_at']