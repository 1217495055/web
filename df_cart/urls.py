#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/19 15:35
# @Author  : Aries
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import *


urlpatterns=[
    url(r'^$',cart),
    url(r'^add(\d+)_(\d+)/$', add),
    url(r'^edit(\d+)_(\d+)/$', edit),
    url(r'^delete(\d+)/$', delete),
]