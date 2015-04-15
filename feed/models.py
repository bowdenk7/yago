from django.db import models
from geoposition.fields import GeopositionField


class VenueClassification(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()

    def __unicode__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()
    cost = models.SmallIntegerField()
    logo_url = models.CharField(max_length=400, unique=True)
    classification = models.ForeignKey(VenueClassification, related_name='classifications')
    district = models.ForeignKey(District, related_name='venues')

    def __unicode__(self):
        return self.name