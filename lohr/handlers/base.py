#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import logging
logging.basicConfig()
import tornado.web
import tornado.gen
import tornadoredis
from lohr import settings, models, utils
import threading

c = tornadoredis.Client(**settings.REDIS_CONNECTION)
c.connect()


class RequestDetailLogger(threading.Thread):
    """ request detail logger in another thread
    """
    def __init__(self, callback=None, *args, **kwargs):
        self.code = kwargs.pop('code')
        self.request = kwargs.pop('request')
        super(RequestDetailLogger, self).__init__(*args, **kwargs)
        self.callback = callback

    @tornado.gen.coroutine
    def run(self):
        # increase request count
        result = yield tornado.gen.Task(c.incr,
                                        settings.URL_REDIRECT_REQUEST_COUNT_REDIS_BASE_NAME.format(code=self.code))
        ip = utils.get_client_ip(self.request)


class RedirectHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, code):
        if not code:
            self.redirect('/')
        else:
            name = settings.URL_CODE_REDIS_BASE_NAME.format(code=code)
            key_exists = yield tornado.gen.Task(c.exists, name)
            if key_exists:
                redirect_url = yield tornado.gen.Task(c.get, name)

                RequestDetailLogger(code=code, request=self.request).start()

                print 'redirect'
                self.redirect(redirect_url)
            else:
                self.redirect('/')


class GenerateHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        url = self.get_argument('url', '')
        if not url:
            self.redirect('/')
        else:
            url_code = yield tornado.gen.Task(models.generate_urlcode, url)
            self.write(url_code)
            self.finish()


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Welcome to Lohr!')