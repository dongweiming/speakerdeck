from celery.decorators import task

@task(ignore_result=True)
def test():
    return 3


@task
def test2():
    return 2
