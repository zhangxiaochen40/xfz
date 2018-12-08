from django import forms
from apps.news.models import News


class NewsCategoryEditFrom(forms.Form):
    pk = forms.IntegerField(error_messages={"required":"必须传入分类的id！"})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category','auth','pub_time']





