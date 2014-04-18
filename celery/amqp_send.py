import amqp

msg_body = 'A text msg'
EXCHANGE_NAME = 'myex'
routing_key='info'

conn = amqp.Connection(host='localhost', userid='dongwm',
                       password='password', virtual_host='myvhost')
ch = conn.channel()
ch.exchange_declare(EXCHANGE_NAME, type='direct')
msg = amqp.Message(msg_body, content_type='text/plain',
                   application_headers={'foo': 7, 'bar': 'its string'})
ch.basic_publish(msg, EXCHANGE_NAME, routing_key)
print " [x] Sent %r:%r" % (routing_key, msg_body)
ch.close()
conn.close()
