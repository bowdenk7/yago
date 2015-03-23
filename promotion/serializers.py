from rest_framework import serializers
from feed.models import Venue


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('user', 'timestamp', 'expiration', 'redeemed')

