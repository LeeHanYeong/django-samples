from django.db import models


class SampleImageModel(models.Model):
    image = models.ImageField(blank=True)
