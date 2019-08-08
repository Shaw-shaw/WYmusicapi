# import djcelery
# djcelery.setup_loader()
# CELERY_IMPORTS=(
#     'app01.tasks',
# )
# #有些情况可以防止死锁
# CELERYD_FORCE_EXECV=True
# # 设置并发worker数量
# CELERYD_CONCURRENCY=4
# #允许重试
# CELERY_ACKS_LATE=True
# # 每个worker最多执行100个任务被销毁，可以防止内存泄漏
# CELERYD_MAX_TASKS_PER_CHILD=100
# # 超时时间
# CELERYD_TASK_TIME_LIMIT=12*30