from rest_framework import serializers
from .models import MessageAnalytics, ClientEngagement, ReportData
from clients.serializers import ClientSerializer
from campaigns.serializers import CampaignSerializer


class MessageAnalyticsSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = MessageAnalytics
        fields = [
            'id', 'message_type', 'date', 'campaign',
            'sent_count', 'delivered_count', 'open_count', 'click_count',
            'unique_open_count', 'unique_click_count',
            'bounce_count', 'complaint_count',
            'delivery_rate', 'open_rate', 'click_rate',
            'updated_at'
        ]
        read_only_fields = ['updated_at', 'delivery_rate', 'open_rate', 'click_rate']


class ClientEngagementSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = ClientEngagement
        fields = [
            'id', 'client',
            'email_sent_count', 'email_open_count', 'email_click_count',
            'whatsapp_sent_count', 'whatsapp_delivered_count', 'whatsapp_read_count',
            'last_email_sent', 'last_email_opened', 'last_email_clicked',
            'last_whatsapp_sent', 'last_whatsapp_delivered', 'last_whatsapp_read',
            'engagement_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['engagement_score', 'created_at', 'updated_at']


class ReportDataSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = ReportData
        fields = [
            'id', 'report_type', 'title', 'description',
            'period_start', 'period_end',
            'campaign', 'client',
            'report_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']