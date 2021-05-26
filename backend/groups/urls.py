from django.urls import path, include
from .views import StudyViewSet, ApplyViewSet, StudyConfirmView, GroupViewSet, ExpireView, BanView, GiveUpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'study', StudyViewSet, 'study')
router.register(r'apply', ApplyViewSet, 'apply')
router.register(r'group', GroupViewSet, 'group')

urlpatterns = [
    path('', include(router.urls)),
    path('confirm/<int:pk>/', StudyConfirmView.as_view(), name='study_confirm'),
    path('expire/<int:pk>/', ExpireView.as_view(), name='study_confirm'),
    path('ban/<int:pk>/', BanView.as_view(), name='ban'),
    path('giveup/<int:pk>/', GiveUpView.as_view(), name='giveup')
]
