#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from . import local_settings

DEBUG = local_settings.DEBUG

REDIS_CONNECTION = local_settings.REDIS_CONNECTION

URL_CODE_REDIS_BASE_NAME = 'redirect:urlcode:{code}'
URL_CODE_ID_REDIS_NAME = 'redirect:url:id'
URL_CODE_SET_NAME = 'redirect:url:all'