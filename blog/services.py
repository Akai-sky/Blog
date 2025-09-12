from .models import ArticleDetail
from .blog_cache import CacheService, CACHE_HIT_COUNTER, CACHE_MISS_COUNTER
from .tasks import async_update_read_stats


class ReadStatsBusinessService:
    @staticmethod
    def record_read(article_id, user_id):
        """记录登录用户的文章阅读行为"""
        total_reads = CacheService.increase_article_total_reads(article_id)
        is_new_visitor = CacheService.increase_total_visitor(article_id, user_id)
        user_read_count = CacheService.increase_user_read_count(user_id, article_id)
        total_visitors = CacheService.get_total_visitors_count(article_id)

        async_update_read_stats.delay(article_id, user_id)

        return {
            "total_reads": total_reads,
            "total_visitors": total_visitors,
            "user_read_count": user_read_count,
            "is_new_visitor": bool(is_new_visitor)
        }

    @staticmethod
    def get_article_stats(article_id):
        """获取文章统计数据"""
        return {
            "total_reads": CacheService.get_article_total_reads(article_id) or 0,
            "total_visitors": CacheService.get_total_visitors_count(article_id) or 0
        }

    @staticmethod
    def get_user_read_history(user_id):
        """获取用户阅读历史"""
        read_details = ArticleDetail.objects.filter(
            user_id=user_id
        ).select_related('article').order_by('-update_time')

        return [{
            "article_id": detail.article.id,
            "title": detail.article.title,
            "read_count": detail.read_count,
            "last_read_time": detail.update_time
        } for detail in read_details]

    @staticmethod
    def get_cache_metrics():
        """获取缓存指标（修正常量引用）"""
        client = CacheService.get_redis_client()
        return {
            "hit_rate": CacheService.get_cache_hit_rate(),
            "hits": int(client.get(CACHE_HIT_COUNTER) or 0),  # 直接使用导入的常量
            "misses": int(client.get(CACHE_MISS_COUNTER) or 0)
        }
