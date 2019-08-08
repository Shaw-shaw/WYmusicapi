from django.test import TestCase

# Create your tests here.
def check_result():
    res = 'ac59669c-0c60-4186-acaa-15331bc74c2c'
    from celery.result import AsyncResult
    from celery_task.celery import app
    async = AsyncResult(id=res, app=app)
    if async.successful():
        # 取出它return的值
        result = async.get()
        print('成功',result)
        return 'ok'
    elif async.failed():
        print('执行失败')
        return '执行失败'
    elif async.status == 'PENDING':
        print('任务等待被执行')
        return '任务等待被执行'
    elif async.status == 'RETRY':
        print('任务异常后正在重试')
        return '任务异常后正在重试'
    elif async.status == 'STARTED':
        print('任务已经开始被执行')
        return '任务已经开始被执行'
if __name__ == '__main__':
    check_result()
