from django.conf.urls import patterns, url
from user_post import views
from yagoapp.urls import router


router.register(r'posts', views.PostViewSet)

urlpatterns = patterns('',

)