# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# 设计购物车模型类
# 用户－－商品（1:n）
# 商品－－用户（１：n）
class CartInfo(models.Model):
    # 引用用户表的外键,
    user=models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    # 引用商品表的外键，
    goods=models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    # 商品数量
    count=models.IntegerField(default=0)