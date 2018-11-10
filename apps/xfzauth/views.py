from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from utils import restful


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, telephone=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth('账户被冻结')
        else:
            return restful.para_error('手机或密码错误')
    else:
        errors = form.get_errors()
        return restful.para_error(message=errors)
