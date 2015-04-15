from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.db.models import Count
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from feed.models import Venue
from account.models import User, Points, POINT_VALUE_FOR_CREATING_POST, POINT_VALUE_FOR_LIKING_POST, POINT_VALUE_FOR_REPORTED_POST
from datetime import datetime, timedelta
from feed.serializers import VenueSerializerWithDistance
from feed.views import calc_distance_in_meters

from user_post.models import Post, ReportedPost, Like, REPORTED_POST_COUNT_THRESHOLD
from user_post.serializers import PostSerializer, ReportedPostSerializer, LikeSerializer, ExtendedPostSerializer
from yagoapp.settings import POSTS_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, MEDIA_ROOT


class PostList(APIView):
    """
    List all posts, or create a new post.

    POST params
    image
    position
    venue
    """
    parser_classes = (MultiPartParser, FileUploadParser,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostList, self).dispatch(*args, **kwargs)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

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

        if 'image' in request.DATA:
            f = request.DATA['image']
        elif 'image' in request.FILES:
            f = request.FILES['image']
        else:
            post.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

        points = Points(user=post.user, venue=post.venue, value=POINT_VALUE_FOR_CREATING_POST)
        user = User.objects.get(pk=points.user.pk)
        user.current_points += points.value
        points.save()
        user.save()

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


@csrf_exempt
@api_view(['GET'])
def get_recent_posts(request):
    """
    Returns a list of all posts made in the last 24 hours, newest first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(timestamp__gte=yesterday).exclude(image_url='').annotate(Count("like")).order_by(
        '-timestamp')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def formatted_time_proximity(timestamp):
    diff = datetime.utcnow().replace(tzinfo=utc) - timestamp
    if diff > timedelta(hours=1):
        return "{0}h".format(diff.seconds / 3600)
    else:
        return "{0}m".format(diff.seconds / 60)


@csrf_exempt
@api_view(['GET'])
def get_top_posts(request):
    """
    Returns a list of all posts made in the last 24 hours, most likes first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(timestamp__gte=yesterday).exclude(image_url='').annotate(
        Count("like")).order_by('-like__count')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_recent_venue_posts(request, pk):
    """
    Returns a list of all posts made for a venue in the last 24 hours, newest first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(venue=pk, timestamp__gte=yesterday).exclude(image_url='').annotate(
        Count("like")).order_by('-timestamp')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_top_venue_posts(request, pk):
    """
    Returns a list of all posts made for a venue in the last 24 hours, most likes first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(venue=pk, timestamp__gte=yesterday).exclude(image_url='').annotate(
        Count("like")).order_by('-like__count')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_recent_district_posts(request, pk):
    """
    Returns a list of all posts made for a venue in the last 24 hours, newest first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(venue__district=pk, timestamp__gte=yesterday).exclude(image_url='').annotate(
        Count("like")).order_by('-timestamp')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_top_district_posts(request, pk):
    """
    Returns a list of all posts made for a venue in the last 24 hours, most likes first
    """
    yesterday = datetime.now() - timedelta(hours=24)
    posts = Post.objects.filter(venue__district=pk, timestamp__gte=yesterday).exclude(image_url='').annotate(
        Count("like")).order_by('-like__count')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

        if reports.count() + 1 >= REPORTED_POST_COUNT_THRESHOLD:
            # if adding it brings the total count to the threshold, we just shouldn't add it and go straight to removing it
            reports.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def toggle_like(request):
    '''
    Log a like for a certain post from a user, if the user has already liked the post, unlike it.

    Return the new like total for that post
    '''
    serializer = LikeSerializer(data={'user': request.user.pk, 'post': int(request.data['post'])})
    if serializer.is_valid():

        like = Like.objects.filter(user=serializer.data['user'], post=serializer.data['post'])
        if like.count() > 0:
            # if the user has already liked the post, unlike the post
            like.delete()
        else:
            post = Post.objects.get(pk=serializer.data['post'])
            points = Points(user=post.user, venue=post.venue, value=POINT_VALUE_FOR_LIKING_POST)
            user = User.objects.get(pk=post.user.pk)
            user.current_points += points.value
            serializer.save()
            points.save()
            user.save()

        return_data = {'total_likes': Like.objects.filter(post=serializer.data['post']).count()}
        return Response(return_data, status=status.HTTP_200_OK, content_type='application/json')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_closest_venues(request, position):
    """
    Returns the closest 3 venues to the passed in geoposition.
    """
    latitude = float(position.split(",")[0])
    longitude = float(position.split(",")[1])

    venues = Venue.objects.all()
    for venue in venues:
        venue.distance = calc_distance_in_meters(float(latitude), float(longitude),
                                                 float(venue.position.latitude),
                                                 float(venue.position.longitude))
    venues.order_by('-distance')
    serializer = VenueSerializerWithDistance(venues[:3], many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)