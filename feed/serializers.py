from rest_framework import serializers
from feed.models import Venue, VenueClassification, District


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('pk', 'name', 'position', 'cost', 'logo_url', 'classification', 'district')

class VenueSerializerWithDistance(VenueSerializer):
    distance = serializers.IntegerField()

    class Meta:
        model = Venue
        fields = fields = ('pk', 'name', 'position', 'cost', 'logo_url', 'classification', 'district', 'distance')

class VenueClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueClassification
        fields = ('pk', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('pk', 'name', 'position')


class DistrictSerializerWithDistance(DistrictSerializer):
    distance = serializers.IntegerField()

    class Meta:
        model = District
        fields = ('pk', 'name', 'position', 'distance')