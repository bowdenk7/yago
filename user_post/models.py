from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from feed.models import Venue


class Post(models.Model):
    image_url = models.CharField(max_length=400, unique=True)
    thumbnail_url = models.CharField(max_length=400, unique=True)
    position = GeopositionField()
    user = models.ForeignKey(User)
    likes = models.SmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    venue = models.ForeignKey(Venue)

