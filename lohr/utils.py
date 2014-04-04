#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'


def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-FORWARDED-FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.headers.get('REMOTE-ADDR', '')
        if not ip:
            ip = request.headers.get('X-Real-IP', '')

    return ip