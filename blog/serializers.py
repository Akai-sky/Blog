from rest_framework import serializers
from .models import Article, ArticleDetail, ArticleReadStats


class ArticleSerializer(serializers.ModelSerializer):
    """文章序列化器，包含阅读统计信息"""
    total_reads = serializers.IntegerField(read_only=True)
    total_visitors = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'total_reads', 'total_visitors']


class ArticleDetailSerializer(serializers.ModelSerializer):
    """用户阅读详情序列化器"""
    article_title = serializers.CharField(source='article.title', read_only=True)

    class Meta:
        model = ArticleDetail
        fields = ['id', 'article', 'article_title', 'read_count', 'update_time']
        read_only_fields = ['id', 'update_time']


class ArticleStatsSerializer(serializers.ModelSerializer):
    """文章统计数据序列化器"""
    article_title = serializers.CharField(source='article.title', read_only=True)

    class Meta:
        model = ArticleReadStats
        fields = ['id', 'article', 'article_title', 'total_reads', 'total_visitors', 'update_time']
        read_only_fields = ['id', 'update_time']
