from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required


def cms_login(request):
    """
    cms登陆界面
    """
    return render(request,'cms/login.html')


@staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')
