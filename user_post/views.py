from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from user_post.models import Post
from user_post.serializers import PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

