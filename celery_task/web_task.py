# # 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from fkw_v1 import settings
from django.core.cache import cache
from apps.web.models import Visitor_Num

# 创建一个Celery类的实列化对象
# 第一个参数可以随便写，通常写路径
# 第二个参数指定存放

# 一定要配置启动文件
import os
import django

# 这一段在wsgi中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fkw_v1.settings")
django.setup()
from celery_task.celery import APP


# 定义任务函数
@APP.task
def statflow():
    num = cache.get('StatFlow')
    Visitor_Num.objects.create(visitor_num=int(num))
