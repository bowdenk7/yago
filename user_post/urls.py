from django.conf.urls import patterns
from user_post import views
from yagoapp.urls import router


router.register(r'posts', views.PostViewSet)

urlpatterns = patterns('',

)