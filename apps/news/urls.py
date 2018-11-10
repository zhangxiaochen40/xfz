from django.urls import path
from .views import index

app_name = 'news'

urlpatterns=[
    path('',index,name='index')
]