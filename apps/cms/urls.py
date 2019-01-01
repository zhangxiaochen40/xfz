from django.urls import path
from .views import cms_login, index, write_news, news_category,add_news_category,edit_news_category,del_news_category
from .views import upload_file,qntoken
from .import course_views

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
    path('banners/', views.banners, name='banners'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('banner_list/', views.banner_list, name='banner_list'),
    path('delete_banner/', views.delete_banner, name='delete_banner'),
    path('edit_banner/', views.edit_banner, name='edit_banner'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('delete_news/', views.delete_news, name='delete_news'),
]

# 发布课程相关的url映射
urlpatterns += [
    path('pub_course', course_views.PubCourseView.as_view(), name='pub_course'),
]