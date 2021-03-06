from django import forms
from apps.news.models import News, Banner
from apps.course.models import Course, CourseCategory


class NewsCategoryEditFrom(forms.Form):
    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id！"})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category','auth','pub_time']


class AddBannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['priority', 'img_url', 'link_to']


class EditBannerForm(forms.ModelForm):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ['priority', 'img_url', 'link_to']


class EditNewsForm(forms.ModelForm):

    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'auth', 'pub_time']


class PubCourseForm(forms.ModelForm):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category','teacher', 'pub_time']




