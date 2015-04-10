from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from user_post import views
from yagoapp.urls import router

router.register(r'reported_posts', views.ReportedPostViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = patterns('',

    url(r'^like_post/$', csrf_exempt(views.toggle_like)),
    url(r'^report_post/$', csrf_exempt(views.report_post)),
    url(r'^recent_posts/$', views.get_recent_posts),
    url(r'^top_posts/$', views.get_top_posts),
    url(r'^recent_venue_posts/(?P<pk>[0-9]+)/$', views.get_recent_venue_posts),
    url(r'^top_venue_posts/(?P<pk>[0-9]+)/$', views.get_top_venue_posts),
    url(r'^recent_district_posts/(?P<pk>[0-9]+)/$', views.get_recent_district_posts),
    url(r'^top_district_posts/(?P<pk>[0-9]+)/$', views.get_top_district_posts),

    url(r'^$', views.PostList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
)