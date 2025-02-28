from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageTemplateViewSet,
    TemplateCategoryViewSet,
    TemplateAttachmentViewSet
)

router = DefaultRouter()
router.register(r'templates', MessageTemplateViewSet)
router.register(r'categories', TemplateCategoryViewSet)
router.register(r'attachments', TemplateAttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]