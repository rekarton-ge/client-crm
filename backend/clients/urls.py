from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ClientTagViewSet, ClientGroupViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'tags', ClientTagViewSet)
router.register(r'groups', ClientGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]