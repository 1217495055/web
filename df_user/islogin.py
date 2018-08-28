# coding=utf-8
from django.http import HttpResponseRedirect


# 如果未登录则转到登录页面
def islogin(func):
    # *args, **kwargs  不影响函数的传入参数
    def login_fun(request, *args, **kwargs):
        # 如果有session则继续执行
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        # 否则，转到登录页面
        else:
            red = HttpResponseRedirect('/user/login')
            # 在 cookie　中存入一个 url,
            # request.path ：表示当前路径
            # request.get_full_path():表示完整路径
            # 登录成功了，则取出url
            red.set_cookie('url', request.get_full_path)
            return red
    return login_fun

