from rest_framework import viewsets
from feed.models import Venue, District
from feed.serializers import VenueSerializer, DistrictSerializer


class VenueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows venues to be viewed or edited.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows districts to be viewed or edited.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

