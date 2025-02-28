from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, ClientTag, ClientGroup
from .serializers import ClientSerializer, ClientTagSerializer, ClientGroupSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    API для работы с клиентами
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'source']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company']
    ordering_fields = ['created_at', 'last_contacted']


class ClientTagViewSet(viewsets.ModelViewSet):
    """
    API для работы с тегами клиентов
    """
    queryset = ClientTag.objects.all()
    serializer_class = ClientTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']


class ClientGroupViewSet(viewsets.ModelViewSet):
    """
    API для работы с группами клиентов
    """
    queryset = ClientGroup.objects.all()
    serializer_class = ClientGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']