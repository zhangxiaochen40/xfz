# _*_ coding:utf-8 _*_

from django import forms
from apps.forms import FormMixin


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=16)
    remember = forms.IntegerField(required=False)

