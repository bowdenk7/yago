from rest_framework import serializers
from user_post.models import Post, ReportedPost, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class PostSerializerWithLikes(PostSerializer):
    like__count = serializers.IntegerField(default=0)


class TotalLikesSerializer(serializers.Serializer):
    total_likes = serializers.IntegerField


class ReportedPostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReportedPost
        fields = ('user', 'post')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post')

