from rest_framework import serializers
from feed.models import Venue, VenueClassification, District


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('pk', 'name', 'position', 'cost', 'logo_url', 'classification', 'district')


class VenueClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueClassification
        fields = ('pk', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        pass

    class Meta:
        model = District
        fields = ('pk', 'name', 'position')