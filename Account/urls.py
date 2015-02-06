from django.conf.urls import patterns, url, include
import views
from yago.urls import router


router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',

    # Attempt to register a new user
    # url(r'^register/$', views.register_user, name='register'),

    # Attempt to log user into session
    # ex. /user/login/
    # url(r'^login/$', views.login_user, name='login'),

    # Log user out of the session
    # ex. /user/logout/
    # url(r'^logout/$', views.logout_user, name='logout'),

)