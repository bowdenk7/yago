from django.conf.urls import patterns, url
from user_post import views
from yagoapp.urls import router

<<<<<<< Updated upstream

router.register(r'posts', views.PostViewSet)
router.register(r'reported_posts', views.ReportedPostViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = patterns('',

    url(r'^create_post/$', views.create_post),
    url(r'^like_post/$', views.like_post),
    url(r'^report_post/$', views.report_post),

    url(r'^$', views.PostList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
)