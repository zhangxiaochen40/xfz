from django.urls import path
from .views import index, news_detail

app_name = 'news'

urlpatterns = [
    path('',index,name='index'),
    path('<int:news_id>', news_detail, name='news_detail')
]