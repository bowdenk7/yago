
from django.db import models
from account.models import User
from feed.models import Venue



class PromotionType(models.Model):
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=400)
    point_cost = models.IntegerField()

    def __unicode__(self):
        return self.name + " at " + str(self.venue)


class Promotion(models.Model):
    user = models.ForeignKey(User, related_name='promotions')
    timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)
    type = models.ForeignKey(PromotionType)
    redeemed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user + "'s " + str(self.type)
