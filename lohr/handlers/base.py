#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import tornado.web
import tornado.gen
import tornadoredis
from lohr import settings, models

c = tornadoredis.Client(**settings.REDIS_CONNECTION)
c.connect()


def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-FORWARDED-FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.headers.get('REMOTE-ADDR', '')
        if not ip:
            ip = request.headers.get('X-Real-IP', '')

    return ip

@tornado.gen.coroutine
def log_request_detail(code, request):
    # incr request count
    result = yield tornado.gen.Task(c.incr, settings.URL_REDIRECT_REQUEST_COUNT_REDIS_BASE_NAME.format(code=code))

    ip = get_client_ip(request)


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

                # log request detail
                yield tornado.gen.Task(log_request_detail, code, self.request)

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