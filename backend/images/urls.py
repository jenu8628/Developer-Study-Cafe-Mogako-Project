from django.urls import path, include
from .views import ImageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'upload', ImageViewSet, 'upload')

urlpatterns = [
    path('',include(router.urls))
]
