###术语

Producers: 生产者发送消息到一个交换机(exchange)
Exchanges: 交换机可以通过routingkey路由消息到消费者
Consumers: 消费者申明队列，绑定到交换上,从上面接收消息
Queues: 队列接收发送到交换的消息
Routing keys: 每个消息都有一个路由键(依赖于交换类型)

1. Direct Exchange

如其名，直接交换，也就是指定一个消息被那个队列接收， 这个消息被celerybeat定义个一个routing key，如果你发送给交换机并且那个队列绑定的bindingkey 那么就会直接转给这个队列

2. Topic Exchange

你设想一下这样的环境(我举例个小型的应该用场景): 你有三个队列和三个消息, A消息可能希望被X,Y处理,B消息你希望被,X,Z处理,C消息你希望被Y,Z处理.并且这个不是队列的不同而是消息希望被相关的队列都去执行,看一张图可能更好理解:

对，Topic可以根据同类的属性进程通配, 你只需要routing key有’.’分割:比如上图中的usa.news, usa.weather, europe.news, europe.weather

3. Fanout Exchange

先想一下广播的概念, 在设想你有某个任务，相当耗费时间，但是却要求很高的实时性,那么你可以需要多台服务器的多个workers一起工作，每个服务器负担其中的一部分,但是celerybeat只会生成一个任务,被某个worker取走就没了, 所以你需要让每个服务器的队列都要收到这个消息.这里很需要注意的是:你的fanout类型的消息在生成的时候为多份,每个队列一份，而不是一个消息发送给单一队列的次数

###celery相关依赖的关系

1. py-amqp amqplib的celery版本,在librabbitmq`pip install librabbitmq`不可用时作为python的模块



```
1. 支持超时
2. 支持心跳
3. 支持rabbitmq的插件
4. 使用AMQP0.9.1替代0.8
5. 更好的错误恢复
…

```

2. billiard 多进程池的扩展
   multiprocessing模块的celery版本

3.  kombu 消息处理框架

   **特性**

   ```
	  1. 支持非amqp协议的传输: Redis, Mongodb, zeroMQ, Zookeeper, in memory等
		 2. 可以使用django的orm和sqlallchemy
			3. 自动编码,序列化和压缩消息体
			   ...
				  ```

4. django-celery(3.1之后以及不必须了)



   1. 使用django的ORM作为任务执行结果的backend
	  2. 增加celery的django命令 python manage.py celery xxx
		 3. 使用django的AdminCURD任务

5. celerymon 一个实时监控celeryworker,使用highchart画图,提供api的tornado页面
6. flower 实时监控celery的任务队列(提供web接口)

**特性**

```
1. 显示任务进程和历史,任务具体信息(参数，开始时间，运行时间等),画图和分析
2. 能远程查看worker状态,关闭或者重启worker实例,控制worker池的大小(自动缩放),查看当前运行的任务，任务周期,取消任务，速率控制,查看配置等
3. 查看celery的队列情况和趋势
4. 提供httpapi
...
```**py-amqp的amqplib区别**


### celery2(2.3.3)+django(2.3.3)-celery+django(1.2.5)

```
mkvirtualenv venv
pip install celery==2.3.3
pip install django==1.2.5
pip install django-celery==2.3.3
pip install celerymon
/Users/dongwm/envs/venv/bin/django-admin.py startproject dongwm
/Users/dongwm/envs/venv/bin/django-admin.py startapp dongwm2
mv dongwm2 dongwm
python dongwm/manage.py syncdb
# 一大推的修改 django 跑起来了
python dongwm/manage.py runserver 0.0.0.0:8000
# 也能访问http://localhost:8000/admin
#添加dongwm2/tasks.py

python dongwm/manage.py celerybeat -l debug 
python dongwm/manage.py celeryd -l debug
python dongwm/manage.py celerycam -l debug
celerymon  --config=settings_real
```

### celery3

```
pip install celery 
pip install flower
pip install sqlalchemy # 为了记录执行结果到sqlite,也可以选mongodb等等
celery -A proj worker -B -Q hipri -l debug
celery flower --broker=amqp://dongwm:password@localhost:5672/myvhost
# 监控和管理
celery purge # 从队列中删除所有消息- 慎用
celery -A proj status tasks.add d19eeb0b-3b9c-4232-957f-b47b6764b967 # 显示任务执行结果
celery -A proj  inspect stats # worker信息统计
celery inspect -d host1,host2 revoked # 多节点被取消的任务
python monitor.py # 实时监控事件状态
```


