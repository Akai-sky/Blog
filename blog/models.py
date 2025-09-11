from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    """博客文章"""
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = models.TextField(verbose_name="文章内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """文章详情"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="read_details")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="read_details")
    read_count = models.PositiveIntegerField(default=1, verbose_name="阅读次数")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后阅读时间")

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = "文章详情"
        ordering = ("id",)


class ArticleReadStats(models.Model):
    """文章阅读统计"""
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="read_stats")
    total_reads = models.PositiveIntegerField(default=0, verbose_name="总阅读次数")
    total_visitors = models.PositiveIntegerField(default=0, verbose_name="总阅读人数")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    class Meta:
        verbose_name = "文章阅读统计"
        verbose_name_plural = "文章阅读统计"
        ordering = ("id",)
