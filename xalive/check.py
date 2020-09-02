# check_res.py

from celery.result import AsyncResult
from app import app

async = AsyncResult(id='bd600820-9366-4220-a679-3e435ae91e71', app=app)

if async.successful():
    result = async.get()
    print(result)

elif async.failed():
    print('执行失败')

elif async.status == 'PENDING':
    print('任务等待中')

elif async.status == 'RETRY':
    print('任务异常后重试')

elif async.status == 'STARTED':
    print('任务正在执行')