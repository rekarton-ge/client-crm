from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageAnalyticsViewSet,
    ClientEngagementViewSet,
    ReportDataViewSet
)

router = DefaultRouter()
router.register(r'message-analytics', MessageAnalyticsViewSet, basename='message-analytics')
router.register(r'client-engagement', ClientEngagementViewSet, basename='client-engagement')
router.register(r'reports', ReportDataViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
]