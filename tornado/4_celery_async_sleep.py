#!/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tcelery
import sleep_task as tasks


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

tcelery.setup_nonblocking_producer()

class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.Task(tasks.sleep.apply_async, args=[5])
        self.write("when i sleep 5s")
        self.finish()

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler), (r"/justnow", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
