from celery import Celery

app = Celery('tasks', broker='amqp://dongwm:password@localhost:5672/myvhost')

@app.task
def add(x, y):
    return x + y
