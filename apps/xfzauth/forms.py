# _*_ coding:utf-8 _*_

from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from apps.xfzauth.models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=16)
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    password1 = forms.CharField(max_length=16)
    password2 = forms.CharField(max_length=16)
    img_captcha = forms.CharField(max_length=4,min_length=4)
    sms_captcha = forms.CharField(max_length=4,min_length=4)

    def clean(self):
        cleaned_data =super(RegisterForm,self).clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致')

        # 图形验证码 验证
        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha.lower())
        if not cache_img_captcha or img_captcha.lower()!=cache_img_captcha:
            raise forms.ValidationError('图片验证码错误')

        sms_captcha = cleaned_data.get('sms_captcha')
        telephone =cleaned_data.get('telephone')
        cache_sms_captcha = cache.get(telephone)
        if not cache_img_captcha or cache_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('手机验证码错误')

        exist = User.object.filter(telephone=telephone).exists()

        if exist:
            raise forms.ValidationError('该手机已经注册')


