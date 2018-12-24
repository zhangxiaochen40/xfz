from rest_framework import serializers
from .models import News, NewsCategory2, Comment, Banner
from apps.xfzauth.serializers import AuthSerializers


class NewsCategorySerializer(serializers.ModelSerializer):
    """
    新闻类别的序列化类
    """
    class Meta:
        model = NewsCategory2
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    """
    新闻的序列化类
    """
    category = NewsCategorySerializer()
    auth = AuthSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'auth')


class CommentSerializer(serializers.ModelSerializer):
    """
    评论的序列化类
    """
    author = AuthSerializers()

    class Meta:
        model = Comment
        fields = ('id','content', 'pub_time', 'author')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'priority', 'img_url', 'link_to']






