from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, CampaignScheduleViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'schedules', CampaignScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]