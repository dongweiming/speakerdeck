from __future__ import absolute_import

from proj.celery import app


@app.task
def add(x, y):
#    raise IOError
    return x + y
