from rest_framework import serializers
from feed.models import Venue, District


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('name', 'district', 'position', 'cost', 'logo_url', 'classification')


class DistrictSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        pass

    class Meta:
        model = District
        fields = ('name', 'position')