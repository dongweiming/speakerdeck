# coding=utf-8
import amqp
from functools import partial

EXCHANGE_NAME = 'myex'

def callback(channel, msg):
    for key, val in msg.properties.items():
        print('%s: %s' % (key, str(val)))
    for key, val in msg.delivery_info.items():
        print('> %s: %s' % (key, str(val)))

    print('')
    print(msg.body)
    print('-------')
    print(msg.delivery_tag)
    channel.basic_ack(msg.delivery_tag)


conn = amqp.Connection(host='localhost', userid='dongwm',
                       password='password', virtual_host='myvhost')
ch = conn.channel()
ch.exchange_declare(exchange=EXCHANGE_NAME, type='direct')
qname, _, _ = ch.queue_declare()
ch.queue_bind(qname, EXCHANGE_NAME, routing_key='info') # binding_key
ch.basic_consume(qname, callback=partial(callback, ch))

# 每次注册一个回调就会在下面的字典中加一项
while ch.callbacks:
    ch.wait()
ch.close()
conn.close()
