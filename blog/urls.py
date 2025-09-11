from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, StatsViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'stats', StatsViewSet, basename='stats')

urlpatterns = [
    path('api/', include(router.urls)),
]
