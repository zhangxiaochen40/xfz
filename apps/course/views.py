from django.shortcuts import render
from .models import Course


def course_index(request):
    """
    课程首页
    :param request:
    :return:
    """
    course_list = Course.objects.all()
    context = {
        'course_list': course_list
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    """
    课程详情页
    :param request:
    :param course_id:
    :return:
    """
    course = Course.objects.get(pk=course_id)
    return render(request, 'course/course_detail.html', {
        'course': course
    })