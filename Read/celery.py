from __future__ import absolute_import
import os

from celery import Celery

#设置环境变量
from Read import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Read.settings')

#创建Celery对象
app = Celery('Read')

# 加载配置
app.config_from_object('django.conf:settings')

# 自动发现task异步任务
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)