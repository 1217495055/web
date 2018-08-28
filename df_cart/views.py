# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from df_user.islogin import islogin
from .models import *
from django.http import JsonResponse

# Create your views here....
# 购物车

# 判断用户是否登录
@islogin
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    lenn = len(carts)
    context = {'title': '购物车',
               'page_name': 1,
               'carts': carts,
               'len': lenn}
    return render(request, 'df_cart/cart.html', context)

# 添加商品


@islogin
def add(request, gid, count):
    # 用户uid购买了gid商品，数量为count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车是否已经有此商品，有则增加数量，没有则添加
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        # cart 购物车商品数量
        cart = carts[0]
        # 直接增加数量
        cart.count = cart.count+count
    # 不存在则直接添加
    else:  
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    # 不管是新买的，还是新建的，都保存进数据库
    cart.save()
    count_s = CartInfo.objects.filter(user_id=uid).count()
    request.session['count'] = count_s
    # 如果是ajax请求则返回json(当前登录的用户的购买数量),否则转向购物车
    if request.is_ajax():
        # count=CartInfo.objects.filter(user_id=request.session['user_id']).count()

        print('*'*10)
        print('ajax')
        #--------------未使用
        return JsonResponse({'count': count_s})
    else:
        return redirect('/cart/')


@islogin
def edit(request, cart_id, count):
    try:
        # 根据　crat_id 找到　cart
        cart = CartInfo.objects.get(pk=int(cart_id))
        # 更改数量
        count1 = cart.count = int(count)
        # 保存进数据库,返回　'ok'
        cart.save()
        data = {'ok': 0}
    # 如果更新失败，返回 count
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)


@islogin
def delete(request, cart_id):
    cart = CartInfo.objects.get(pk=int(cart_id))
    cart.delete()
    # data={'ok':1}
    # except Exception as e:
    count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    request.session['count'] = count
    data = {'count': count}
    return JsonResponse(data)



