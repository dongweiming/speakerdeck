#!/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

EXECUTOR = ThreadPoolExecutor(max_workers=4)

def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
                ).add_done_callback(
                    lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                        partial(callback, future)))
    return wrapper


class SleepHandler(tornado.web.RequestHandler):
    @unblock
    def get(self):
        time.sleep(5)
        return "when i sleep %s s".format(5)


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
