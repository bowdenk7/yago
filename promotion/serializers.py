from rest_framework import serializers
from promotion.models import PromotionType, Promotion


class PromotionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionType
        fields = ('venue', 'name', 'description', 'point_cost')


class PromotionFeedSerializer(serializers.Serializer):
    venue_name = serializers.CharField()
    name = serializers.CharField()
    point_cost = serializers.IntegerField()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('user', 'timestamp', 'expiration', 'type', 'redeemed')

