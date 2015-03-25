from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from user_post.models import Post, ReportedPost, Like, REPORTED_POST_COUNT_THRESHOLD
from user_post.serializers import PostSerializer, ReportedPostSerializer, LikeSerializer
from django.db.models import Count


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ReportedPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reported posts to be viewed or edited.
    """
    queryset = ReportedPost.objects.all()
    serializer_class = ReportedPostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows likes to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


@api_view(['POST'])
def create_post(request):
    '''
    Create a post for a venue
    '''
    serializer = PostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def report_post(request):
    '''
    Report a post. If that post has been reported three times, remove it.

    A user can only report an image once. It cannot be unreported.

    In this implementation, if a post has been reported one less time than the threshold,
    instead of adding it then checking and deleting it, we just delete it.
    '''
    serializer = ReportedPostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():

        reports = ReportedPost.objects.filter(post=int(serializer.data['post'].split('/')[-2]))

        if reports.filter(user=int(serializer.data['user'].split('/')[-2])).count() > 0:
            # if the user has already reported the post
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        if reports.count()+1 >= REPORTED_POST_COUNT_THRESHOLD:
            # if adding it brings the total count to the threshold, we just shouldn't add it and go straight to removing it
            reports.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def like_post(request):
    '''
    Log a like for a certain post from a user, if the user has already liked the post, unlike it
    '''
    serializer = LikeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():

        like = Like.objects.filter(user=int(serializer.data['user'].split('/')[-2]), post=int(serializer.data['post'].split('/')[-2]))
        if like.count() > 0:
            # if the user has already liked the post, unlike the post
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)