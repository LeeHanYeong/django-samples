from django.db import models


class SampleBase64ImageModel(models.Model):
    image = models.ImageField(blank=True)


class SampleBase64FileModel(models.Model):
    file = models.FileField(blank=True)
