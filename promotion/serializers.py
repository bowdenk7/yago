from rest_framework import serializers
from promotion.models import PromotionType, Promotion


class PromotionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionType
        fields = ('venue', 'name', 'description', 'point_cost')


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('user', 'timestamp', 'expiration', 'type', 'redeemed')

