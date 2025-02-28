from rest_framework import serializers
from .models import Campaign, CampaignSchedule
from clients.serializers import ClientSerializer, ClientGroupSerializer
from templates.serializers import MessageTemplateSerializer


class CampaignScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSchedule
        fields = [
            'id', 'campaign', 'schedule_type', 'scheduled_time',
            'days_of_week', 'time_of_day', 'is_active',
            'created_at', 'updated_at'
        ]


class CampaignSerializer(serializers.ModelSerializer):
    client_group = ClientGroupSerializer(read_only=True)
    clients = ClientSerializer(many=True, read_only=True)
    email_template = MessageTemplateSerializer(read_only=True)
    whatsapp_template = MessageTemplateSerializer(read_only=True)
    schedules = CampaignScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'type',
            'client_group', 'clients',
            'email_template', 'whatsapp_template',
            'is_scheduled', 'scheduled_start', 'scheduled_end',
            'frequency', 'custom_schedule', 'status',
            'max_messages_per_day', 'total_recipients',
            'sent_count', 'delivered_count', 'read_count', 'error_count',
            'created_at', 'updated_at', 'started_at', 'completed_at',
            'schedules'
        ]
        read_only_fields = [
            'created_at', 'updated_at',
            'started_at', 'completed_at',
            'total_recipients', 'sent_count',
            'delivered_count', 'read_count', 'error_count'
        ]