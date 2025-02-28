from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Campaign, CampaignSchedule
from .serializers import CampaignSerializer, CampaignScheduleSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API для работы с кампаниями
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['type', 'status', 'frequency', 'is_scheduled']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'started_at', 'completed_at']

    def perform_create(self, serializer):
        """
        Кастомная логика создания кампании
        """
        campaign = serializer.save()
        # Здесь можно добавить дополнительную логику при создании кампании
        return campaign


class CampaignScheduleViewSet(viewsets.ModelViewSet):
    """
    API для работы с расписанием кампаний
    """
    queryset = CampaignSchedule.objects.all()
    serializer_class = CampaignScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['campaign', 'schedule_type', 'is_active']
    ordering_fields = ['scheduled_time', 'created_at']