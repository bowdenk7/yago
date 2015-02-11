from rest_framework import serializers
from django.contrib.auth.models import User
from user_post.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(queryset=Post.objects.all(),
                                                view_name='post-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'posts')
