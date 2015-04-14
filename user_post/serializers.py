from rest_framework import serializers
from user_post.models import Post, ReportedPost, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class ExtendedPostSerializer(PostSerializer):
    like__count = serializers.IntegerField(default=0)
    time_text = serializers.StringRelatedField()


class ReportedPostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReportedPost
        fields = ('user', 'post')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post')

