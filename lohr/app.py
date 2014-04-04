#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from lohr.handlers import *

define("port", default=8888, type=int)
define("config_file", default="app_config.yml", help="app_config file")


class Application(tornado.web.Application):
    def __init__(self, **overrides):
        handlers = [(r'/', IndexHandler),
                    (r'/go/(\w+)', RedirectHandler),
                    (r'/gen/', GenerateHandler),
                    ]

        tornado.web.Application.__init__(self, handlers)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()