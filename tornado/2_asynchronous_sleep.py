#!/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop

import time

def test(t, callback=None, **kwargs):
    future = tornado.concurrent.Future()
    return future

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + 5, callback=self.on_response)
    def on_response(self):
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
