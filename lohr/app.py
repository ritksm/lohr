#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.dirname(BASE_DIR))  # append to PYTHONPATH

import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from lohr.handlers import *
import settings

define("port", default=8888, type=int)
define("config_file", default="app_config.yml", help="app_config file")


class Application(tornado.web.Application):
    def __init__(self, **overrides):
        handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings.STATIC_ROOT}),
            (r'/', IndexHandler),
            (r'/go/(\w+)', RedirectHandler),
            (r'/generate/', GenerateHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()