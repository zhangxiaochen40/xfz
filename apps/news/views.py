from django.shortcuts import render
from .models import News,NewsCategory2


def index(request):
    news_list = News.objects.all()
    category_list = NewsCategory2.objects.all()
    context = {
        'news_list': news_list,
        'category_list': category_list
    }
    return render(request,'news/index.html',context=context)


def news_detail(request, news_id):
    return render(request,'news/news_detail.html')


def search(request):
    return render(request, 'search/search.html')
