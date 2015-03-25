from rest_framework import serializers
from feed.models import Venue, VenueClassification, District


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ('name', 'position', 'cost', 'logo_url', 'classification', 'district')


class VenueClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueClassification
        fields = ('name')


class DistrictSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        pass

    class Meta:
        model = District
        fields = ('name', 'position')