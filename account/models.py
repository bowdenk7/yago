from django.contrib.auth.models import AbstractUser
from django.db import models
from feed.models import Venue


class User(AbstractUser):
    current_points = models.IntegerField(default=0)


class Points(models.Model):
    user = models.ForeignKey(User)
    venue = models.ForeignKey(Venue)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()
