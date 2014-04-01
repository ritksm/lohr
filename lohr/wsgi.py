#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import tornado.ioloop
import tornado.web
from lohr.views import *


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/go/(\w+)', RedirectHandler),
    (r'/gen/', GenerateHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()