from django.db import models
from timezone_field import TimeZoneField


class Post(models.Model):
    dt = models.DateTimeField()
    timezone = TimeZoneField()
