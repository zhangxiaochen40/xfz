from django.shortcuts import render
from .models import PayInfoModel


def payinfo(request):
    """
    付费页面
    :param request:
    :return:
    """
    context = {
        'payinfos': PayInfoModel.objects.all()
    }
    return render(request,'payinfo/payinfo.html', context=context)







