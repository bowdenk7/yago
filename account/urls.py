from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from account import views
from yagoapp.urls import router


router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',

    url(r'^register-by-token/$', views.social_register, name='register'),
    url(r'^users_feed/$', csrf_exempt(views.get_users_feed)),
    url(r'^users_feed/(?P<limit>[0-9]+)$', csrf_exempt(views.get_limited_users_feed)),
    url(r'^recent_user_posts/(?P<user>[0-9]+)$', csrf_exempt(views.get_recent_user_posts)),
    url(r'^top_user_posts/(?P<user>[0-9]+)$', csrf_exempt(views.get_top_user_posts)),
    url(r'^user_likes/(?P<user>[0-9]+)$', csrf_exempt(views.get_user_likes)),
    url(r'^user_promotion_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_user_promotion_feed)),
    url(r'^user_redeemed_promotion_feed/(?P<pk>[0-9]+)$', csrf_exempt(views.get_user_redeemed_promotion_feed)),

    # Attempt to register a new user
    # url(r'^register/$', views.register_user, name='register'),

    # Attempt to log user into session
    # ex. /user/login/
    # url(r'^login/$', views.login_user, name='login'),

    # Log user out of the session
    # ex. /user/logout/
    # url(r'^logout/$', views.logout_user, name='logout'),

)