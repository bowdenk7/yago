from django.contrib.auth.models import AbstractUser
from django.db import models
from feed.models import Venue

POINT_VALUE_FOR_CREATING_POST = 10
POINT_VALUE_FOR_LIKING_POST = 1
POINT_VALUE_FOR_REPORTED_POST = -1 * (POINT_VALUE_FOR_CREATING_POST + 5)

class User(AbstractUser):
    current_points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username


class Points(models.Model):
    user = models.ForeignKey(User)
    venue = models.ForeignKey(Venue)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()

    def __unicode__(self):
        return self.user.username + " - " + str(self.value) + " points"