from rest_framework import viewsets
from promotion.models import Promotion
from promotion.serializers import PromotionSerializer


class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

