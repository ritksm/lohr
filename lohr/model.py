#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import basehash
import tornadoredis
import tornado.gen
from . import settings

c = tornadoredis.Client(**settings.REDIS_CONNECTION)
c.connect()

@tornado.gen.coroutine
def generate_urlcode(redirect_url):
    new_id = yield tornado.gen.Task(c.incr, settings.URL_CODE_ID_REDIS_NAME)
    code = basehash.base62().encode(new_id)

    # set redis cache
    yield tornado.gen.Task(c.sadd, settings.URL_CODE_SET_NAME, code)
    yield tornado.gen.Task(c.set,
                           settings.URL_CODE_REDIS_BASE_NAME.format(code=code),
                           redirect_url)

    raise tornado.gen.Return(code)