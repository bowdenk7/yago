from rest_framework import serializers
from user_post.models import Post, ReportedPost, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post


class ReportedPostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReportedPost
        fields = ('user', 'post')


class LikeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post')

