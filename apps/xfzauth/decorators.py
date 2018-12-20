# _*_ coding:utf-8 _*_

from utils import restful
from django.shortcuts import redirect


def xfz_login_require(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message="请先登陆")
            else:
                return redirect('/')
    return wrapper