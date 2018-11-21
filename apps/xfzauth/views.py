from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
from apps.xfzauth.models import User


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


@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username =form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password1')
        user = User.object.create_user(telephone=telephone,username=username,password=pwd)
        login(request,user)
        return restful.ok()
    else:
        return restful.para_error(message=form.get_errors())


def logout_view(request):
    """
    退出登陆
    :param request:
    :return:
    """
    logout(request)
    return redirect(reverse('index'))


def img_captcha(request):
    """
    验证码图片
    :param request:
    :return:
    """
    text,image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)

    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone,code,5*60)
    print('短信验证码：',code)
    print(code)
    # result = aliyunsms.send_sms('telephone','code')
    return restful.ok()
    # print(result)
    # return HttpResponse('success')


def cache_test(request):
    cache.set('zxczxc','1213123',5*60)
    result =cache.get('zxczxc')
    print(result)
    return HttpResponse('success')
