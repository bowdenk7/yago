from django.conf.urls import patterns
from promotion import views
from yagoapp.urls import router


router.register(r'promotions', views.PromotionViewSet)

urlpatterns = patterns('',

)