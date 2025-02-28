from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger документации API
schema_view = get_schema_view(
   openapi.Info(
      title="CRM API",
      default_version='v1',
      description="API для клиентской CRM-системы с возможностью рассылки сообщений",
      contact=openapi.Contact(email="admin@example.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    # path('api/clients/', include('clients.urls')),
    # path('api/messaging/', include('messaging.urls')),
    # path('api/templates/', include('templates.urls')),
    # path('api/campaigns/', include('campaigns.urls')),
    # path('api/analytics/', include('analytics.urls')),
]

# Добавляем URL маршруты для обработки медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)