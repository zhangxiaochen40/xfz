from django.shortcuts import render
from .models import News, NewsCategory2, Comment, Banner
from .serializers import NewsSerializer, CommentSerializer
from django.conf import settings
from utils import restful
from django.http import Http404
from .forms import CommentForm
from apps.xfzauth.decorators import xfz_login_required


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    news_list = News.objects.select_related('category', 'auth').all()[0:count]
    category_list = NewsCategory2.objects.all()
    context = {
        'news_list': news_list,
        'category_list': category_list,
        'banners': Banner.objects.all()
    }
    return render(request,'news/index.html', context=context)


def news_list(request):
    """
    新闻列表
    :param request:
    :return:
    """
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start+settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('category', 'auth').all()[start:end]
    else:
        newses = News.objects.filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses,many=True)
    data =serializer.data
    return restful.result(data=data)


@xfz_login_required
def comment(request):
    """
    评论
    :param request:
    :return:
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        # 应该加个try catch
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(news=news, content=content, author=request.user)
        # 序列化
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.para_error(message=form.get_errors())


def news_detail(request, news_id):
    """
    新闻详情
    :param request:
    :param news_id:
    :return:
    """
    try:
        news_detail = News.objects.select_related('category', 'auth').get(id=news_id)
        context = {
            'news_detail': news_detail
        }
        return render(request, 'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404


def search(request):
    return render(request, 'search/search.html')
