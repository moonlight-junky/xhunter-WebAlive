from kombu import Queue, Exchange
from datetime import timedelta

CELERY_QUEUES = (
    Queue("ascan", Exchange("ascan"), routing_key="ascan"),
    Queue("save", Exchange("save"), routing_key="save")
)

CELERY_ROUTES = (
    [
        (
            "xalive.tasks.send_request",
            {"queue": "ascan", "routing_key": "ascan"},
        ),
        (
            "xalive.tasks.save_results",
            {"queue": "save", "routing_key": "save"},
        ),
    ],
)

BROKER_URL = "redis://123.57.43.21:16379/0"  # 使用redis 作为消息代理

CELERY_RESULT_BACKEND = "redis://123.57.43.21:16379/0"  # 任务结果存在Redis

CELERY_RESULT_SERIALIZER = "json"  # 读取任务结果序列化

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间

CELERY_IMPORTS = (     # 指定导入的任务模块,可以指定多个
    'xalive.tasks',
)
