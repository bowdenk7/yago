from django.conf.urls import patterns
from feed import views
from yagoapp.urls import router


router.register(r'venues', views.VenueViewSet)
router.register(r'districts', views.DistrictViewSet)

urlpatterns = patterns('',

)