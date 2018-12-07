from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


class NewsCategory2(models.Model):
    name = models.CharField(max_length=100)
