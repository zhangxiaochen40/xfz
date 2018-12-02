from django.urls import path
from .views import cms_login, index, write_news, news_category

app_name='cms'

urlpatterns = [
    path('login/', cms_login, name='login'),
    path('index/', index, name='index'),
    path('write_news/', write_news.as_view(), name='write_news'),
    path('news_category/', news_category, name='news_category'),
]