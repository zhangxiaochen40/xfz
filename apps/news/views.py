from django.shortcuts import render
from .models import News,NewsCategory2
from .serializers import NewsSerializer
from django.conf import settings
from utils import restful
from django.http import Http404


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    news_list = News.objects.select_related('category','auth').all()[0:count]
    category_list = NewsCategory2.objects.all()
    context = {
        'news_list': news_list,
        'category_list': category_list
    }
    return render(request,'news/index.html',context=context)


def news_list(request):
    """
    新闻列表
    :param request:
    :return:
    """
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start+settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('category','auth').all()[start:end]
    else:
        newses = News.objects.filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses,many=True)
    data =serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news_detail = News.objects.select_related('category','auth').get(id=news_id)
        context = {
            'news_detail': news_detail
        }
        return render(request, 'news/news_detail.html',context=context)
    except:
        raise Http404




def search(request):
    return render(request, 'search/search.html')
