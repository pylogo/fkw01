from celery import Celery
from datetime import timedelta

broker = 'redis://:'
backend = 'redis://:'

APP = Celery('test', broker=broker, backend=backend,
             include=[
                 'celery_task.user_task',
                 'celery_task.web_task',
             ])

APP.conf.beat_schedule = {
    # 名字随意命名
    'add-every-60-seconds': {
        'task': 'celery_task.web_task.statflow',
        'schedule': timedelta(seconds=60*60),
        # 传递参数
        'args': ()
    },
}
