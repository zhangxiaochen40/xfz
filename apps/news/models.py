from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


class NewsCategory2(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('NewsCategory2',on_delete=models.SET_NULL,null=True)
    auth = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering=['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News',on_delete=models.CASCADE)
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
