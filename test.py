#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-28 19:41:46
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"
