from django.db import models


class PayInfoModel(models.Model):
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=300)
    path = models.FilePathField()
    price = models.FloatField()







