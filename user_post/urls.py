from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from user_post import views
from yagoapp.urls import router

router.register(r'reported_posts', views.ReportedPostViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = patterns('',

    url(r'^like_post/$', csrf_exempt(views.like_post)),
    url(r'^report_post/$', csrf_exempt(views.report_post)),
    url(r'^create_post/$', csrf_exempt(views.create_post)),

    url(r'^$', views.PostList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
)