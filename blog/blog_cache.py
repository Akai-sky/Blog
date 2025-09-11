from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)
REDIS_CLIENT = get_redis_connection('default')

# 文章总阅读量
ARTICLE_TOTAL_READS = "article:{article_id}:total_reads"
# 用户阅读文章次数
USER_READ_COUNT = "user:{user_id}:article:{article_id}:count"
# 文章阅读人数
ARTICLE_TOTAL_VISITORS = "article:{article_id}:total_visitors"
# 缓存命中计数
CACHE_HIT_COUNTER = "stats:cache:hits"
# 缓存未命中计数
CACHE_MISS_COUNTER = "stats:cache:misses"


class CacheService:
    @staticmethod
    def get_redis_client():
        return get_redis_connection('default')

    @staticmethod
    def increase_article_total_reads(article_id):
        """增加文章阅读数"""
        key = ARTICLE_TOTAL_READS.format(article_id=article_id)
        return REDIS_CLIENT.incr(key)

    @staticmethod
    def get_article_total_reads(article_id):
        """文章总阅读量"""
        key = ARTICLE_TOTAL_READS.format(article_id=article_id)
        value = REDIS_CLIENT.get(key)
        if value is not None:
            REDIS_CLIENT.incr(CACHE_HIT_COUNTER)
            return int(value)
        REDIS_CLIENT.incr(CACHE_MISS_COUNTER)
        return None

    @staticmethod
    def increase_user_read_count(user_id, article_id):
        """增加用户阅读次数"""
        key = USER_READ_COUNT.format(user_id=user_id, article_id=article_id)
        if not REDIS_CLIENT.exists(key):
            REDIS_CLIENT.set(key, 1)
            return 1
        return REDIS_CLIENT.incr(key)

    @staticmethod
    def get_user_read_count(user_id, article_id):
        """用户阅读次数"""
        key = USER_READ_COUNT.format(user_id=user_id, article_id=article_id)
        value = REDIS_CLIENT.get(key)
        if value is not None:
            REDIS_CLIENT.incr(CACHE_HIT_COUNTER)
            return int(value)
        REDIS_CLIENT.incr(CACHE_MISS_COUNTER)
        return None

    @staticmethod
    def increase_total_visitor(article_id, user_id):
        """增加总阅读人数"""
        key = ARTICLE_TOTAL_VISITORS.format(article_id=article_id)
        return REDIS_CLIENT.sadd(key, user_id)

    @staticmethod
    def get_total_visitors_count(article_id):
        """总阅读人数"""
        key = ARTICLE_TOTAL_VISITORS.format(article_id=article_id)
        return REDIS_CLIENT.scard(key)

    @staticmethod
    def get_cache_hit_rate():
        """缓存命中率（命中/(命中+未命中)）"""
        hits = int(REDIS_CLIENT.get(CACHE_HIT_COUNTER) or 0)
        misses = int(REDIS_CLIENT.get(CACHE_MISS_COUNTER) or 0)
        total = hits + misses
        return hits / total if total > 0 else 0.0

    @staticmethod
    def delete_article_cache(article_id):
        """删除某篇文章的所有缓存"""
        keys = [
            ARTICLE_TOTAL_READS.format(article_id=article_id),
            ARTICLE_TOTAL_VISITORS.format(article_id=article_id)
        ]
        REDIS_CLIENT.delete(*keys)
