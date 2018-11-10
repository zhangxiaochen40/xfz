from django.urls import path
from .views import cms_login

app_name='cms'

urlpatterns = [
    path('login/', cms_login,name='login')
]