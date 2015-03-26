from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from feed.models import Venue

from user_post.models import Post, ReportedPost, Like, REPORTED_POST_COUNT_THRESHOLD
from user_post.serializers import PostSerializer, ReportedPostSerializer, LikeSerializer
from yagoapp.settings import POSTS_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, MEDIA_ROOT


class PostList(APIView):
    """
    List all posts, or create a new post.

    POST params
    image
    position
    venue
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostList, self).dispatch(*args, **kwargs)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        image_url = ""
        thumbnail_url = ""

        #need to generate a pk
        post = Post(image_url="",
                    thumbnail_url="",
                    position=request.data['position'],
                    user=request.user,
                    venue=Venue.objects.get(pk=int(request.data['venue'])))
        post.save()

        f = request.data['file']
        image_string = f.read()

        #TODO generate thumbnail

        #TODO add error handling

        image_url = POSTS_URL + post.venue.name + "/" + str(post.pk) + ".png"
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        key.key = image_url
        key.set_contents_from_string(image_string)

        data = dict()
        data['image_url'] = image_url
        data['thumbnail_url'] = thumbnail_url
        data['user'] = request.user
        data['position'] = request.data['position']
        data['venue'] = request.data['venue']
        post.image_url = MEDIA_ROOT + image_url
        post.thumbnail_url = thumbnail_url
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetail(APIView):
    """
    Retrieve or delete a post instance.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostDetail, self).dispatch(*args, **kwargs)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
