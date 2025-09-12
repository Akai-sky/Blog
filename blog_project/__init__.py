import pymysql
pymysql.install_as_MySQLdb()  # 让 Django 把 pymysql 当作 MySQLdb 使用

from .celery import app as celery_app

__all__ = ('celery_app',)
