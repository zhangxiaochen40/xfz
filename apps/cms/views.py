from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET,require_POST
from apps.news.models import NewsCategory2,News
from utils import restful
from .forms import NewsCategoryEditFrom,WriteNewsForm
import os
from django.conf import settings
import qiniu
from qiniu import auth,Auth


def cms_login(request):
    """
    cms登陆界面
    """
    return render(request,'cms/login.html')


# @staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')


class write_news(View):
    """
    添加新闻
    """
    def get(self,request):
        category_list=NewsCategory2.objects.all()
        return render(request,'cms/write_news.html',{
            'category_list':category_list
        })

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory2.objects.get(pk=category_id)
            content = form.cleaned_data.get('content')
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,category=category,content=content, auth=request.User.username)
            return restful.ok()
        else:
            return restful.para_error(message=form.get_errors())


def banners(request):
    """
    轮播图
    :param request:
    :return:
    """
    return render(request,'cms/banners.html')


@require_GET
def news_category(request):
    """
    新闻类别
    :param request:
    :return:
    """
    category_list=NewsCategory2.objects.all()
    return render(request,'cms/news-category.html',{
        'category_list':category_list
    })


@require_POST
def add_news_category(request):
    """
    添加新闻类别
    :param request:
    :return:
    """
    name =request.POST.get('name')
    exist = NewsCategory2.objects.filter(name=name).exists()
    if not exist:
        NewsCategory2.objects.create(name=name)
        return restful.ok()
    else:
        return restful.para_error(message="已经存在该类别")


@require_POST
def edit_news_category(request):
    """
    编辑新闻的类别
    :param request:
    :return:
    """
    forms = NewsCategoryEditFrom(request.POST)
    if forms.is_valid():
        pk = forms.cleaned_data.get('pk')
        name = forms.cleaned_data.get('name')
        try:
            NewsCategory2.objects.filter(pk=pk).update(name=name)
            return restful.ok()

        except:
            return restful.para_error(message='该分类不存在！')
    else:
        return restful.para_error(forms.get_error())


@require_POST
def del_news_category(request):
    """
    删除新闻类别
    :param request:
    :return:
    """
    name =request.POST.get('name')
    try:
        NewsCategory2.objects.filter(name=name).delete()
        return restful.ok()
    except:
        return restful.para_error(message='删除失败')


@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name =file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 构建完整的上传的图片的地址
    url = request.build_absolute_uri(settings.MEDIA_ROOT+name)
    return restful.result(data={'url':url})


@require_GET
def qntoken(request):
    access_key = 'Qz4h7_q5efLZMyP4vkLgSRxCFNuMJdhPaQVUfPEu'
    secret_key = 'ZUJE1YHLF435PloH_sBgLuiybCvod-7gkYNoAsRI'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'zwork'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    return restful.result(data={'token':token})


