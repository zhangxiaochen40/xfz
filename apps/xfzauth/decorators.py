# _*_ coding:utf-8 _*_
from utils import restful
from django.shortcuts import redirect


def xfz_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth("请先登陆")
            else:
                return redirect('/')
    return wrapper


