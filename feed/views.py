from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from feed.models import Venue, VenueClassification, District
from feed.serializers import VenueSerializer, VenueClassificationSerializer, DistrictSerializer
from user_post.models import Post
from user_post.serializers import PostSerializer
from django.db.models import Count, F
from math import sin, cos, atan2, sqrt

class VenueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows venues to be viewed or edited.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueClassificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows venues to be viewed or edited.
    """
    queryset = VenueClassification.objects.all()
    serializer_class = VenueClassificationSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows districts to be viewed or edited.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


# @list_route(methods=['get'])
@api_view(['GET'])
@csrf_exempt
def get_district_feed(request, pk):
    """
    Returns a list of all venues for a particular district

    e.g. input Buckhead, get back Moondogs, Red Door, Hole in the Wall, etc.
    """
    # Getting error, think related to no posts for a venue?
    # venues = Venue.objects.filter(district=pk
    #     ).annotate(post_count=Count("post")
    #     ).order_by('-post_count')
    venues = Venue.objects.filter(district=pk)
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_location_feed(request, position):
    """
    Returns a list of districts within a certain mile radius

    e.g. input location near Atlanta, get back Buckhead, Highlands, and Edgewood


    **Params**:

    position: float value pair, e.g. 33.4,-84.5

    **Does not currently work**
    """
    latitude = float(position.split(",")[0])
    longitude = float(position.split(",")[1])

    districts = District.objects.annotate(
            distance=calc_distance_in_meters(float(latitude), float(longitude), F('position__latitude'), F('position__longitude'))
        ).order_by('-distance')
    serializer = VenueSerializer(districts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def calc_distance_in_meters(lat1, long1, lat2, long2):
    # http://andrew.hedges.name/experiments/haversine/
    R = 6373000
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = (sin(dlat/2.0))^2 + cos(lat1) * cos(lat2) * (sin(dlong/2.0))^2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


@api_view(['GET'])
def get_bar_feed(request, pk):
    """
    Returns a list of images for a particular bar

    e.g. input Moondogs, get back Image1 with 10 likes, Image2 with 8 likes, etc.
    """
    posts = Post.objects.filter(venue=pk
        ).annotate(like_count=Count("like")
        ).order_by('-like_count')
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_highlights_feed(request, pk):
    """
    Returns a list of images for a particular district

    e.g. input Buckhead, get back Image9 with 30 likes, Image3 with 17 likes, etc.
    """
    posts = Post.objects.filter(venue__district=pk
        ).annotate(like_count=Count("like")
        ).order_by('-like_count')
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)