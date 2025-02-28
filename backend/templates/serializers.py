from rest_framework import serializers
from .models import MessageTemplate, TemplateCategory, TemplateAttachment


class TemplateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateCategory
        fields = ['id', 'name', 'description', 'created_at']


class TemplateAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateAttachment
        fields = ['id', 'file', 'filename', 'content_type', 'created_at']


class MessageTemplateSerializer(serializers.ModelSerializer):
    categories = TemplateCategorySerializer(many=True, read_only=True)
    attachments = TemplateAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = MessageTemplate
        fields = [
            'id', 'name', 'description', 'type',
            'subject', 'body', 'is_html',
            'variables', 'is_active',
            'created_at', 'updated_at',
            'categories', 'attachments'
        ]
        read_only_fields = ['created_at', 'updated_at']