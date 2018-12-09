from rest_framework import serializers
from .models import News,NewsCategory2
from apps.xfzauth.serializers import AuthSerializers


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory2
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategory2()
    auth = AuthSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'auth')





