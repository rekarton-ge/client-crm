from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, MessageAttachment, MessageEvent
from .serializers import (
    MessageSerializer,
    MessageAttachmentSerializer,
    MessageEventSerializer
)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API для работы с сообщениями
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['type', 'direction', 'status', 'client', 'campaign']
    search_fields = ['subject', 'body', 'from_email', 'to_email', 'from_number', 'to_number']
    ordering_fields = ['created_at', 'sent_at', 'delivered_at', 'read_at']


class MessageAttachmentViewSet(viewsets.ModelViewSet):
    """
    API для работы с вложениями сообщений
    """
    queryset = MessageAttachment.objects.all()
    serializer_class = MessageAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['message', 'content_type']
    search_fields = ['filename']


class MessageEventViewSet(viewsets.ModelViewSet):
    """
    API для работы с событиями сообщений
    """
    queryset = MessageEvent.objects.all()
    serializer_class = MessageEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['message', 'event_type']
    search_fields = ['ip_address', 'user_agent']
    ordering_fields = ['occurred_at']