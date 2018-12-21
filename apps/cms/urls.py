from django.urls import path
from .views import cms_login, index, write_news, news_category,add_news_category,edit_news_category,del_news_category
from .views import upload_file,qntoken

from . import views
app_name = 'cms'

urlpatterns = [
    path('login/', cms_login, name='login'),
    path('index/', index, name='index'),
    path('write_news/', write_news.as_view(), name='write_news'),
    path('news_category/', news_category, name='news_category'),
    path('add_news_category/', add_news_category, name='add_news_category'),
    path('edit_news_category/', edit_news_category, name='edit_news_category'),
    path('del_news_category/', del_news_category, name='del_news_category'),
    path('upload_file/', upload_file, name='upload_file'),
    path('token/',qntoken,name='qntoken'),
    path('banners', views.banners, name='banners'),
]