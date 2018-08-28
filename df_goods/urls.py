#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *


urlpatterns=[
    url(r'^$',index),
    #第一个值的type id 的标号，第二个值是第几页，第三个值是排序的依据
    url(r'^list(\d+)_(\d+)_(\d+)/$',goodlist),
    url(r'^(\d+)/$', detail),
    url(r'^search/$', MySearchView()),
]
app_name = 'pizzerias'