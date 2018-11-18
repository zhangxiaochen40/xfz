from django.urls import path
from .views import login_view,logout_view,img_captcha,sms_captcha

app_name = 'xzfauth'

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('img_captcha/', img_captcha, name='img_captcha'),
    path('sms_captcha/', sms_captcha, name='sms_captcha'),
]