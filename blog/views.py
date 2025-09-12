from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, ArticleReadStats
from .serializers import ArticleSerializer, ArticleStatsSerializer, CacheMetricsSerializer
from .services import ReadStatsBusinessService


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """文章视图集，提供文章列表和详情接口"""
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def read(self, request, pk=None):
        """记录文章阅读行为"""
        article = self.get_object()
        stats = ReadStatsBusinessService.record_read(
            article_id=article.id,
            user_id=request.user.id
        )

        serializer = self.get_serializer(article)
        data = serializer.data
        data.update(stats)
        return Response(data)


class StatsViewSet(viewsets.ViewSet):
    """统计数据视图集"""

    @action(detail=False, methods=['get'])
    def article_stats(self, request):
        """获取所有文章的统计数据"""
        stats = ArticleReadStats.objects.all().select_related('article')
        serializer = ArticleStatsSerializer(stats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def cache_metrics(self, request):
        """获取缓存指标数据"""
        metrics = ReadStatsBusinessService.get_cache_metrics()
        serializer = CacheMetricsSerializer(metrics)
        return Response(serializer.data)
