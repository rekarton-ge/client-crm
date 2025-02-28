from rest_framework import serializers
from .models import Message, MessageAttachment, MessageEvent
from clients.serializers import ClientSerializer
from campaigns.serializers import CampaignSerializer
from templates.serializers import MessageTemplateSerializer


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'filename', 'file_size', 'content_type', 'created_at']


class MessageEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageEvent
        fields = ['id', 'event_type', 'occurred_at', 'ip_address', 'user_agent', 'url', 'metadata']


class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)
    template = MessageTemplateSerializer(read_only=True)

    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    events = MessageEventSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'type', 'direction', 'client', 'from_email', 'from_number',
            'to_email', 'to_number', 'subject', 'body', 'has_attachments',
            'status', 'status_details', 'track_opens', 'track_clicks',
            'campaign', 'template', 'created_at', 'scheduled_at',
            'sent_at', 'delivered_at', 'read_at',
            'attachments', 'events'
        ]
        read_only_fields = ['created_at', 'sent_at', 'delivered_at', 'read_at']