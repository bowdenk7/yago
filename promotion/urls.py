from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from promotion import views
from yagoapp.urls import router


router.register(r'promotion_types', views.PromotionTypeViewSet)
router.register(r'promotions', views.PromotionViewSet)

urlpatterns = patterns('',

    url(r'^promotion_type_feed/$', csrf_exempt(views.get_promotion_type_feed)),
    url(r'^venue_promotion_type_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_venue_promotion_type_feed)),
    url(r'^district_promotion_type_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_district_promotion_type_feed)),

    url(r'^purchase_promotion/$', csrf_exempt(views.purchase_promotion)),
    url(r'^redeem_promotion/$', csrf_exempt(views.redeem_promotion)),
)