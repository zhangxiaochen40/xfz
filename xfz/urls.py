"""xfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from apps.news.views import search,index
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('news/', include('apps.news.urls')),
    path('search/', include('haystack.urls')),
    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.xfzauth.urls')),
    path('course/', include('apps.course.urls')),
    path('payinfo/', include('apps.payinfo.urls')),
    path('ueditor/',include('apps.ueditor.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(path('__debug__/',include(debug_toolbar.urls)))
