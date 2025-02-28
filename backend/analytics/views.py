from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MessageAnalytics, ClientEngagement, ReportData
from .serializers import (
    MessageAnalyticsSerializer,
    ClientEngagementSerializer,
    ReportDataSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response


class MessageAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра аналитики сообщений
    """
    queryset = MessageAnalytics.objects.all()
    serializer_class = MessageAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['message_type', 'campaign', 'date']
    ordering_fields = ['date', 'sent_count', 'delivery_rate', 'open_rate']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Получение сводной аналитики
        """
        queryset = self.filter_queryset(self.get_queryset())

        summary = {
            'total_sent': queryset.aggregate(total=models.Sum('sent_count'))['total'] or 0,
            'total_delivered': queryset.aggregate(total=models.Sum('delivered_count'))['total'] or 0,
            'avg_delivery_rate': queryset.aggregate(avg=models.Avg('delivery_rate'))['avg'] or 0,
            'avg_open_rate': queryset.aggregate(avg=models.Avg('open_rate'))['avg'] or 0,
        }

        return Response(summary)


class ClientEngagementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра вовлеченности клиентов
    """
    queryset = ClientEngagement.objects.all()
    serializer_class = ClientEngagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['client']
    ordering_fields = ['engagement_score']

    @action(detail=False, methods=['get'])
    def top_engaged(self, request):
        """
        Получение топ-клиентов по вовлеченности
        """
        queryset = self.filter_queryset(self.get_queryset())
        top_clients = queryset.order_by('-engagement_score')[:10]

        serializer = self.get_serializer(top_clients, many=True)
        return Response(serializer.data)


class ReportDataViewSet(viewsets.ModelViewSet):
    """
    API для работы с отчетами
    """
    queryset = ReportData.objects.all()
    serializer_class = ReportDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['report_type', 'campaign', 'client']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'period_start', 'period_end']

    @action(detail=False, methods=['get'])
    def recent_reports(self, request):
        """
        Получение последних созданных отчетов
        """
        queryset = self.filter_queryset(self.get_queryset())
        recent_reports = queryset.order_by('-created_at')[:5]

        serializer = self.get_serializer(recent_reports, many=True)
        return Response(serializer.data)