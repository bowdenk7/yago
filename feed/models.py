from django.db import models
from geoposition.fields import GeopositionField


class VenueClassification(models.Model):
    name = models.CharField(max_length=100)


class District(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()


class Venue(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()
    cost = models.SmallIntegerField()
    logo_url = models.CharField(max_length=400, unique=True)
    classification = models.ForeignKey(VenueClassification)
    district = models.ForeignKey(District, related_name="venues")
