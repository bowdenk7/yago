from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from feed.models import Venue


class Post(models.Model):
    image_url = models.CharField(max_length=400, unique=True)
    thumbnail_url = models.CharField(max_length=400, unique=True)
    position = GeopositionField()
    user = models.ForeignKey(User, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    venue = models.ForeignKey(Venue)


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)