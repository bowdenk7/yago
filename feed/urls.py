from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from feed import views
from yagoapp.urls import router


router.register(r'venues', views.VenueViewSet)
router.register(r'venue_classifications', views.VenueClassificationViewSet)
router.register(r'districts', views.DistrictViewSet)

urlpatterns = patterns('',

    url(r'^recent_district_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_recent_district_feed)),
    url(r'^top_district_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_top_district_feed)),
    url(r'^location_feed/(?P<position>(-?\d+\.\d+),(-?\d+\.\d+)+)$', views.get_location_feed)


)