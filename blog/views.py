from rest_framework import viewsets
from .models import Article, ArticleReadStats
from .serializers import ArticleSerializer, ArticleStatsSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """文章视图集，提供文章列表和详情接口"""
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer


class StatsViewSet(viewsets.ModelViewSet):
    """统计数据视图集"""
    queryset = ArticleReadStats.objects.all().order_by('-update_time')
    serializer_class = ArticleStatsSerializer

