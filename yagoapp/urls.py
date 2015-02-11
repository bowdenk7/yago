from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('account.urls', namespace='account')),

    url(r'^feed/', include('feed.urls', namespace='feed')),

    url(r'^post/', include('user_post.urls', namespace='post')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^', include(router.urls))
)
