from django.shortcuts import render


def cms_login(request):
    """
    cms登陆界面
    """
    return render(request,'cms/login.html')
