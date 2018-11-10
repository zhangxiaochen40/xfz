from django.shortcuts import render


def payinfo(request):
    """
    付费页面
    :param request:
    :return:
    """
    return render(request,'payinfo/payinfo.html')