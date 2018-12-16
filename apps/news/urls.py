from django.urls import path
from .views import index, news_detail, news_list, comment

app_name = 'news'

urlpatterns = [
    path('',index, name='index'),
    path('list/', news_list,name='news_list'),
    path('<int:news_id>', news_detail, name='news_detail'),
    path('comment', comment, name='comment'),
]