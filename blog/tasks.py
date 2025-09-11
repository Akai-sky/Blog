from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from .models import Article, ArticleDetail, ArticleReadStats

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def async_update_read_stats(self, article_id, user_id):
    """异步更新数据库中的阅读统计"""
    try:
        with transaction.atomic():
            # 是否第一次阅读文章
            first_read = False

            # 更新用户阅读次数
            try:
                detail = ArticleDetail.objects.get(user_id=user_id, article_id=article_id)
                detail.read_count += 1
                detail.save()
            except ArticleDetail.DoesNotExist:
                detail = ArticleDetail.objects.create(
                    user_id=user_id,
                    article_id=article_id,
                    read_count=1
                )
                first_read = True

            # 更新文章总统计
            try:
                stats = ArticleReadStats.objects.get(article_id=article_id)
                stats.total_reads += 1
                if first_read:
                    stats.total_visitors += 1
                stats.save()
            except ArticleReadStats.DoesNotExist:
                stats = ArticleReadStats.objects.create(
                    article_id=article_id,
                    total_reads=1,
                    total_visitors=1 if first_read else 0
                )

        logger.info(f"文章{article_id}统计更新：用户{user_id}阅读{detail.read_count}次，总阅读{stats.total_reads}次")
        return {"status": "success", "article_id": article_id}

    except Exception as e:
        logger.error(f"更新失败：{str(e)}")
        self.retry(exc=e, countdown=5)


@shared_task
def sync_cache_to_db(article_id):
    from .blog_cache import CacheService

    try:
        # 从缓存获取数据
        total_reads = CacheService.get_article_total_reads(article_id) or 0
        total_visitors = CacheService.get_total_visitors_count(article_id) or 0

        # 同步到数据库
        with transaction.atomic():
            try:
                stats = ArticleReadStats.objects.get(article_id=article_id)
                stats.total_reads = total_reads
                stats.total_visitors = total_visitors
                stats.save()
            except ArticleReadStats.DoesNotExist:
                ArticleReadStats.objects.create(
                    article_id=article_id,
                    total_reads=total_reads,
                    total_visitors=total_visitors
                )

        logger.info(f"文章{article_id}缓存同步完成：总阅读{total_reads}，独立访客{total_visitors}")
        return True

    except Exception as e:
        logger.error(f"同步失败：{str(e)}")
        return False

@shared_task
def sync_cache_to_db_all():
    """同步缓存到数据库"""
    article_ids = Article.objects.values_list('id', flat=True)
    for article_id in article_ids:
        sync_cache_to_db.delay(article_id)
    return f"全量同步启动，共 {len(article_ids)} 篇文章"