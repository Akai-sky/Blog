from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article, ArticleReadStats, ArticleDetail

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')

@admin.register(ArticleReadStats)
class ArticleReadStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'total_reads', 'total_visitors')
    readonly_fields = ('update_time',)

@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article', 'read_count', 'update_time')
    readonly_fields = ('update_time',)
