from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageAttachmentViewSet, MessageEventViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'attachments', MessageAttachmentViewSet)
router.register(r'events', MessageEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]