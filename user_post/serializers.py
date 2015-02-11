from rest_framework import serializers
from user_post.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ('image_url', 'thumbnail_url', 'position', 'position', 'user', 'timestamp', 'venue')
