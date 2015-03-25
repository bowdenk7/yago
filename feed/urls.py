from django.conf.urls import patterns, url
from feed import views
from yagoapp.urls import router


router.register(r'venues', views.VenueViewSet)
router.register(r'venue_classifications', views.VenueClassificationViewSet)
router.register(r'districts', views.DistrictViewSet)

urlpatterns = patterns('',

    url(r'^district_feed/(?P<pk>[0-9]+)$', views.get_district_feed),
    url(r'^bar_feed/(?P<pk>[0-9]+)$', views.get_bar_feed),
    url(r'^highlights_feed/(?P<pk>[0-9]+)$', views.get_highlights_feed),
    # location feed does not work properly
    url(r'^location_feed/(?P<position>\-?[0-9]+\.?[0-9]+\,\-?[0-9]+\.?[0-9]+)$', views.get_location_feed)


)