from django.urls import path, include
from .views import BoardViewSet, ArticleView, ArticleDetailView, CommentView, CommentDetailView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'board', BoardViewSet, 'board')


urlpatterns = [
    path('', include(router.urls)),
    path('<int:board>/article/', ArticleView.as_view(), name='articles'),
    path('<int:board>/article/<int:pk>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('<int:board>/article/<int:article>/comment/', CommentView.as_view(), name='comments'),
    path('<int:board>/article/<int:article>/comment/<int:pk>/', CommentDetailView.as_view(), name='comments_detail')
]
