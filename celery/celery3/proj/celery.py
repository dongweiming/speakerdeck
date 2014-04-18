#coding=utf-8
from __future__ import absolute_import

from datetime import timedelta
from celery import Celery

app = Celery('proj',
             broker='amqp://dongwm:password@localhost:5672/myvhost',
             include=['proj.tasks']) # 这里不要设置backend 否则下面的设置不生效

app.conf.update(
    CELERYBEAT_MAX_LOOP_INTERVAL = 10,
    CELERY_RESULT_BACKEND = 'mongodb://localhost:27017',
    CELERY_MONGODB_BACKEND_SETTINGS = {
        'database': 'mydb',
        'taskmeta_collection': 'my_taskmeta_collection',
    },
    #CELERY_RESULT_BACKEND = 'db+sqlite:///results.db',
    CELERY_ROUTES = {
        'proj.tasks.add': {'queue': 'hipri'},
       },

    CELERYBEAT_SCHEDULE = {
        "add": {
               "task": "proj.tasks.add",
                "schedule": timedelta(seconds=3),
                "args": (16, 16)
                        },    },
                )

if __name__ == '__main__':
    app.start()
