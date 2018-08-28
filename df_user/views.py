# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from hashlib import sha1
from django.http import JsonResponse
from .islogin import islogin
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator
from df_cart.models import *


#当收到　register/　请求时，跳转到用户注册页面
def register(request):
    return render(request, 'df_user/register.html')


#当收到　register_handle/　请求时，对注册进行处理
def register_handle(requst):
    response = HttpResponse()
    # 接收用户输入的信息，以 post 的方式进行传输
    post = requst.POST
    #用户名
    uname = post.get('user_name')
    #密码
    upwd = post.get('pwd')
    #确认密码
    ucpwd = post.get('cpwd')
    #电子邮箱
    uemail = post.get('email')

    #判断密码跟确认密码是否相同
    if upwd != ucpwd:
        #如果不同,则重定向到注册页面
        return redirect('/user/register/')

    #对密码进行加密存储
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login/')
   

# 根据前端发送的　Ajax　判断用户名是够已经存在
def register_exist(requset):
    #获取请求中的用户名
    uname = requset.GET.get('uname')
    print(uname)
    #从数据库查询是否有该用户名
    count = UserInfo.objects.filter(uname=uname).count()
    print(count)
    return JsonResponse({'count': count})


# 登录界面
def login(request):
    #如果 cookie 里面存有 uname 则直接显示
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0,
               'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


# 登录处理
def login_handle(request):
    # 接收请求信息
    #用户名
    uname = request.POST.get('username')
    #密码
    upwd = request.POST.get('pwd')
    #是否记住密码(0　不记住，1记住)
    jizhu = request.POST.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # 判断：如果未查到：则用户名错，
    #查到用户名:再判断密码是否正确，正确则转到用户中心
    if len(users) == 1:
        #对密码进行加密
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        # 判断加密输入的密码和查询的密码是否相同
        if s1.hexdigest() == users[0].upwd:
            #跳转到用户中心
            red = HttpResponseRedirect('/user/info')
            count = CartInfo.objects.filter(user_id=users[0].id).count()

            # 记住用户名
            if jizhu != 0:
                # 将　uname　存进cookie
                red.set_cookie('uname', uname)
                red.set_cookie('id',users[0].id)
            else:
                # 不记住密码，清空　cookie　，max_age:设置cookie马上过期
                red.set_cookie('uname', '', max_age=-1)
            # 判断用户是否登录过
            # 将用户名的id,name,count 存入session
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            request.session['count'] = count
            return red
        else:
            #'error_name': １　表示用户名错误
            # 'error_pwd': 1  表示密码错误
            context = {'title': '用户登录', 'error_name': 0,
                       'error_pwd': 1, 'uname': uname,'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1,
                   'error_pwd': 0, 'uname': uname,'upwd':upwd}
        return render(request, 'df_user/login.html', context)


# 如果没登录，则转向登录页
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
    # 在　COOKIES 中读取最近浏览的商品的　id 
    goods_ids = request.COOKIES.get('goods_ids', '')
    #将每个　id 以（，）分割
    goods_id_list = goods_ids.split(',')
    goods_list = []
    if len(goods_ids):
        # 遍历每个　id 
        for goods_id in goods_id_list:
            # 对每个　id 进行查询,再依次加入列表
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'user_address': user_address,
               'page_name': 1, 'info': 1,
               'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)


# 订单
@islogin
def order(request):
    context = {'title': '用户中心', 'page_name': 1, 'order': 1}
    return render(request, 'df_user/user_center_order.html', context)


# 收货地址
@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1, 'site': 1}
    return render(request, 'df_user/user_center_site.html', context)


def logout(request):
    if "user_id" in request.session and "user_name" in request.session:
        # 将id和uphone的值．从session 中移除出去
        del request.session["user_id"]
        del request.session["user_name"]
        # 判断cookies中是否存在登录信息，在决定是否清空
        if "uname" in request.COOKIES and "id" in request.COOKIES:
            resp.delete_cookie("id")
            resp.delete_cookie("uname")
        return redirect('/')
    # 退出后，转向首页
    return redirect('/')


@islogin
def user_center_order(request, pageid):
    """
    此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
    根据用户订单是否支付、下单顺序进行排序
    """

    uid = request.session.get('user_id')
    # 订单信息，根据是否支付、下单顺序进行排序
    orderinfos = OrderInfo.objects.filter(
        user_id=uid).order_by('zhifu', '-oid')

    # 分页
    # 获取orderinfos list  以两个为一页的 list
    paginator = Paginator(orderinfos, 2)
    # 获取 上面集合的第 pageid 个 值
    orderlist = paginator.page(int(pageid))
    # 获取一共多少 页
    plist = paginator.page_range
    # 3页分页显示
    qian1 = 0
    hou = 0
    hou2 = 0
    qian2 = 0
    # dd = dangqian ye
    dd = int(pageid)
    lenn = len(plist)
    if dd > 1:
        qian1 = dd-1
    if dd >= 3:
        qian2 = dd-2
    if dd < lenn:
        hou = dd+1
    if dd+2 <= lenn:
        hou2 = dd+2

    # 构造上下文
    context = {'page_name': 1, 'title': '全部订单', 'pageid': int(pageid),
               'order': 1, 'orderlist': orderlist, 'plist': plist,
               'pre': qian1, 'next': hou, 'pree': qian2, 'lenn': lenn, 'nextt': hou2}

    return render(request, 'df_user/user_center_order.html', context)
