from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET,require_POST
from apps.news.models import NewsCategory2
from utils import restful
from .forms import NewsCategoryEditFrom


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


