# -*- coding: utf-8 -*-
# Create your models here.
from __future__ import unicode_literals
from django.db import models


class UserInfo(models.Model):
    #用户名
    uname = models.CharField(max_length=20)
    #密码
    upwd = models.CharField(max_length=40)
    #电子邮箱
    uemail = models.CharField(max_length=30)
    #收件人(只维护一个地址)
    ushou = models.CharField(max_length=20, default='')
    #详细地址
    uaddress = models.CharField(max_length=100, default='')
    #邮编
    uyoubian = models.CharField(max_length=6, default='')
    #手机号码
    uphone = models.CharField(max_length=11, default='')

