import random
import string
from time import sleep
from kombu.mixins import ConsumerMixin
from kombu import Exchange, Queue
from kombu.pools import producers
from kombu.log import get_logger
from kombu.utils import kwdict, reprcall

logger = get_logger(__name__)
task_exchange = Exchange('tasks', type='direct')
task_queues = [Queue('hp', task_exchange, routing_key='hp'),
               Queue('mp', task_exchange, routing_key='mp'),
               Queue('lp', task_exchange, routing_key='lp')]
priority_to_routing_key = ['hp', 'mp', 'lp']


class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues,
                         accept=['pickle', 'json'],
                         callbacks=[self.process_task])]
    def process_task(self, body, message):
        func = body['func']
        args = body['args']
        kwargs = body['kwargs']
        logger.info('Got task: %s', reprcall(func.__name__, args, kwargs))
        try:
            func(args, **kwdict(kwargs))
        except Exception as exc:
            logger.error('task raised exception: %r', exc)
        message.ack()


def send_as_task(connection, func, args, kwargs={}, level=1):
    payload = {'func': func, 'args': args, 'kwargs': kwargs}
    routing_key = priority_to_routing_key[level]

    with producers[connection].acquire(block=True) as producer:
        producer.publish(payload,
                         serializer='pickle',
                         compression='bzip2',
                         exchange=task_exchange,
                         declare=[task_exchange],
                         routing_key=routing_key)


def gen_tasks():
    while 1:
        choice = random.randint(0, 2)
        args = random.sample(string.ascii_letters, 3)
        send_as_task(conn, test_task, args, kwargs={}, level=choice)
        sleep(1)

def test_task(what=""):
    print("Test for %s" % (what, ))


if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    setup_logging(loglevel='INFO', loggers=[''])
    conn = Connection('mongodb://localhost:27017/kombudtata')
    import billiard
    p = billiard.Process(target=gen_tasks)
    p.start()
    with conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye!!!')
