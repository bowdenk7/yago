from rest_framework import serializers
from django.contrib.auth.models import User
from user_post.models import Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'pk')
