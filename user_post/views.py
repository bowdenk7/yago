from rest_framework import viewsets
from user_post.models import Post
from user_post.serializers import PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

