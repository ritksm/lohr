#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import basehash
import tornado.web
import tornado.gen
import tornadoredis
from . import settings, model

c = tornadoredis.Client(**settings.REDIS_CONNECTION)
c.connect()


class RedirectHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, code):
        if not code:
            self.redirect('/')
        else:
            name = settings.URL_CODE_REDIS_BASE_NAME.format(code=code)
            key_exists = yield tornado.gen.Task(c.exists, name)
            if key_exists:
                redirect_url = yield tornado.gen.Task(c.get, name)
                self.redirect(redirect_url)
            else:
                self.redirect('/')


class GenerateHandler(tornado.web.RequestHandler):
    def generate_callback(self, url_code):
        self.write(url_code)
        self.finish()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        url = self.get_argument('url', '')
        if not url:
            self.redirect('/')
        else:
            model.generate_urlcode(url, self.generate_callback)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Welcome to Lohr!')