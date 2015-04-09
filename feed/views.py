from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from feed.models import Venue, VenueClassification, District
from feed.serializers import VenueSerializer, VenueClassificationSerializer, DistrictSerializer
from user_post.models import Post
from user_post.serializers import PostSerializer
from django.db.models import Count, F
from math import radians, cos, sin, sqrt
# from scipy.spatial import KDTree


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


@csrf_exempt
@api_view(['GET'])
def get_recent_district_feed(request, pk):
    """
    Returns a list of all venues for a particular district, newest first

    e.g. input Buckhead, get back Moondogs, Red Door, Hole in the Wall, etc.
    """
    venues = Venue.objects.filter(district=pk).order_by('-timestamp')
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_top_district_feed(request, pk):
    """
    Returns a list of all venues for a particular district, most likes first

    e.g. input Buckhead, get back Moondogs, Red Door, Hole in the Wall, etc.
    """
    venues = Venue.objects.filter(district=pk).annotate(Count("post")).order_by('-post__count')
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
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
        distance=calc_distance_in_meters(float(latitude), float(longitude), F('position__latitude'),
                                         F('position__longitude'))
    ).order_by('-distance')
    serializer = VenueSerializer(districts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Constants defined by the World Geodetic System 1984 (WGS84)
# http://stackoverflow.com/questions/20654918/python-how-to-speed-up-calculation-of-distances-between-cities
A = 6378.137
B = 6356.7523142
ESQ = 6.69437999014 * 0.001


def geodetic2ecef(lat, lon, alt=0):
    """Convert geodetic coordinates to ECEF."""
    lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - ESQ * sin(lat))
    x = (A / xi + alt) * cos(lat) * cos(lon)
    y = (A / xi + alt) * cos(lat) * sin(lon)
    z = (A / xi * (1 - ESQ) + alt) * sin(lat)
    return x, y, z


def euclidean_distance(distance):
    """Return the approximate Euclidean distance corresponding to the
    given great circle distance (in km).

    """
    return 2 * A * sin(distance / (2 * B))


def calc_distance_in_meters(lat1, long1, lat2, long2):
    # http://andrew.hedges.name/experiments/haversine/
    R = 6373000
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = (sin(dlat / 2.0)) ^ 2 + cos(lat1) * cos(lat2) * (sin(dlong / 2.0)) ^ 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c