from django.contrib import admin
from feed.models import VenueClassification, Venue, District


admin.site.register(VenueClassification)

admin.site.register(Venue)

admin.site.register(District)