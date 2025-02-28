from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MessageTemplate, TemplateCategory, TemplateAttachment
from .serializers import (
    MessageTemplateSerializer,
    TemplateCategorySerializer,
    TemplateAttachmentSerializer
)


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """
    API для работы с шаблонами сообщений
    """
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['type', 'is_html', 'is_active']
    search_fields = ['name', 'description', 'subject', 'body']
    ordering_fields = ['created_at', 'updated_at']


class TemplateCategoryViewSet(viewsets.ModelViewSet):
    """
    API для работы с категориями шаблонов
    """
    queryset = TemplateCategory.objects.all()
    serializer_class = TemplateCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']


class TemplateAttachmentViewSet(viewsets.ModelViewSet):
    """
    API для работы с вложениями шаблонов
    """
    queryset = TemplateAttachment.objects.all()
    serializer_class = TemplateAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['template', 'content_type']
    search_fields = ['filename']
    ordering_fields = ['created_at']