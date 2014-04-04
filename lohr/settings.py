#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import local_settings

DEBUG = local_settings.DEBUG

REDIS_CONNECTION = local_settings.REDIS_CONNECTION

STATIC_ROOT = local_settings.STATIC_ROOT

URL_CODE_REDIS_BASE_NAME = 'redirect:urlcode:{code}'
URL_CODE_ID_REDIS_NAME = 'redirect:url:id'
URL_CODE_SET_NAME = 'redirect:url:all'

URL_REDIRECT_REQUEST_COUNT_REDIS_BASE_NAME = 'redirect:url:request:count:{code}'

HOST = local_settings.HOST