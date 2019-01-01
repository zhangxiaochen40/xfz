from django.shortcuts import render
from django.views import View
from apps.cms.forms import PubCourseForm
from apps.course.models import CourseCategory, Teacher, Course
from utils import restful


def pub_course(request):
    return render(request,'cms/pub_course.html')


class PubCourseView(View):
    """
    发布课程
    """
    def get(self, request):
        return render(request, 'cms/pub_course.html', {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        })

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            category_id = form.cleaned_data.get('category_id')
            teacher_id = form.cleaned_data.get('teacher_id')
            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, price=price,
                                  duration=duration, profile=profile, category=category, teacher=teacher)
            return restful.ok()
        else:
            return restful.para_error(message=form.get_errors())







