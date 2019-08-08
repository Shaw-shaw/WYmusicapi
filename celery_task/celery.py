#必须叫celery，生成celery对象
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
broker='redis://127.0.0.1:6379/0' # 设置
backend='redis://127.0.0.1:6379/1'
# 实例化Celery对象
app=Celery('test',broker=broker,backend=backend,
           # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
           include=['celery_task.send_email_task',
                    ]
           )
# 在当前目录下创建配置文件用下面一行代码导入配置信息
# app.config_from_object('proj.config')
#配置文件app.conf
# 时区问题
# app.conf.beat_schedule = {
#     # 名字随意命名
#     'add-every-10-seconds': {
#         # 执行tasks1下的test_celery函数
#         'task': 'celery_task.order_task.order_add',
#         # 每隔2秒执行一次
#         # 'schedule': 1.0,
#         # 'schedule': crontab(minute="*/1"),
#         'schedule': timedelta(seconds=2),
#         # 传递参数
#         'args': (5,6)
#     },
    # 'add-every-12-seconds': {
    #     'task': 'celery_task.order_task.order_add',
    #     # 每年4月11号，8点42分执行
    #     'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
    #     # 'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
    #     'args': (16, 16)
    # },
# }
# ceshi
# yun gai de 
# yungaide 2
# 云端测试3