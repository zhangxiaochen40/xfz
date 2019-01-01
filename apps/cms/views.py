from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET,require_POST
from apps.news.models import NewsCategory2, News, Banner
from utils import restful
from .forms import NewsCategoryEditFrom, WriteNewsForm, AddBannerForm, EditBannerForm, EditNewsForm
import os
from django.conf import settings
import qiniu
from qiniu import auth, Auth
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse


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
    def get(self, request):
        category_list = NewsCategory2.objects.all()
        return render(request, 'cms/write_news.html', {
            'category_list': category_list
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
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail,category=category,
                                content=content, auth=request.user)
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
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 构建完整的上传的图片的地址
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return restful.result(data={'url': url})


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


def add_banner(request):
    """
    添加轮播图
    :param request:
    :return:
    """

    forms = AddBannerForm(request.POST)
    if forms.is_valid():
        priority = forms.cleaned_data.get('priority')
        img_url = forms.cleaned_data.get('img_url')
        link_to = forms.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority,img_url=img_url,link_to=link_to)
        return restful.result(data={"banner_id":banner.pk})
    else:
        return restful.para_error(message=forms.get_errors())


def banner_list(request):
    """
    轮播图列表
    :param request:
    :return:
    """
    banners = Banner.objects.all()
    serializers = BannerSerializer(banners, many=True)
    return restful.result(data=serializers.data)


def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


def edit_banner(request):
    """
    编辑轮播图
    :param request:
    :return:
    """
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        img_url = form.cleaned_data.get('img_url')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(pk=pk).update(priority=priority, img_url=img_url, link_to=link_to)
        return restful.ok()
    else:
        return restful.para_error(message=form.get_errors())


class NewsListView(View):

    def get(self, request):
        # 当前页
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', '0') or 0)
        news = News.objects.select_related('category', 'auth').all()

        if start or end:
            if start:
                start_data = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_data = datetime(year=2018,month=12,day=15)
            if end:
                end_data = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_data = datetime.today()
            news = news.filter(pub_time__range=(make_aware(start_data), make_aware(end_data)))

        if title:
            news = news.filter(title__icontains=title)

        if category_id:
            news = news.filter(category=category_id)

        paginator = Paginator(news, page)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        context = {
            'categories': NewsCategory2.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&'+parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }
        context.update(context_data)
        return render(request, 'cms/news_list.html', context=context)


    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class EditNewsView(View):
    """
    编辑新闻
    """
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        category = NewsCategory2.objects.all()
        return render(request,'cms/write_news.html',{
            'news': news,
            'category_list': category
        })

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory2.objects.get(pk=category_id)
            content = form.cleaned_data.get('content')
            News.objects.filter(pk=pk).update(title=title, desc=desc, thumbnail= thumbnail, content=content, category=category)
            return restful.ok()
        else:
            return restful.para_error(message=form.get_errors())


@require_POST
def delete_news(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()






