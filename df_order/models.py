# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# 订单表
class OrderInfo(models.Model):
    # 订单编号
    oid = models.CharField(max_length=20, primary_key=True)
    # 下单者
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    # 下单日期
    odate = models.DateTimeField(auto_now=True)
    # 是否支付
    oIsPay = models.IntegerField(default=0)
    # 总价
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    # 收货地址
    oaddress = models.CharField(max_length=150, default='')
    # 金额
    zhifu = models.IntegerField(default=0)

# 订单详表
class OrderDetailInfo(models.Model):
    # 商品
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    # 属于哪个订单表的详表
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    # 价格
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 数量
    count = models.IntegerField()

