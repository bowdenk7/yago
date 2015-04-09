from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField
from feed.models import Venue


class PromotionType(models.Model):
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=400)
    point_cost = models.IntegerField()
    # TODO add images and other supporting meta data


class Promotion(models.Model):
    user = models.ForeignKey(User, related_name='promotions')
    timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)
    type = models.ForeignKey(PromotionType)
    redeemed = models.BooleanField(default=False)
