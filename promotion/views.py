from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from promotion.models import PromotionType, Promotion
from promotion.serializers import PromotionTypeSerializer, PromotionSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class PromotionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PromotionType.objects.all()
    serializer_class = PromotionTypeSerializer


class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


@csrf_exempt
@api_view(['GET'])
def get_promotion_type_feed(request):
    """
    Returns a list of all promotions

    e.g. get back promotions about free cover and discounts anywhere
    """
    promotions = PromotionType.objects.all().order_by('-point_cost')
    serializer = PromotionTypeSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_venue_promotion_type_feed(request, pk):
    """
    Returns a list of all promotions for a particular venue

    e.g. input Red Door, get back promotions about free cover and discounts at Red Door
    """
    promotions = PromotionType.objects.filter(venue=pk).order_by('-point_cost')
    serializer = PromotionTypeSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_district_promotion_type_feed(request, pk):
    """
    Returns a list of all promotions for a particular district

    e.g. input Buckhead, get back promotions about free cover and discounts at Red Door, Moondogs, etc.
    """
    promotions = PromotionType.objects.filter(venue__district=pk).order_by('-point_cost')
    serializer = PromotionTypeSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_user_promotion_feed(request, pk):
    """
    Returns a list of all unredeemed promotions "purchased" by a particular user

    e.g. input user ID, get back promotions about free cover and discounts that have not yet been redeemed
    """
    promotions = Promotion.objects.filter(user=pk, redeemed=False).order_by('-expiration')
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_user_promotion(request, pk):
    """
    Returns an unredeemed promotions "purchased" by a particular user

    e.g. input promotion ID that promotion if unredeemed
    """
    promotion = Promotion.objects.get(pk=pk).exclude(redeemed=True)
    serializer = PromotionSerializer(promotion)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def purchase_promotion(request):
    '''
    Log a promotion purchased by a user
    '''
    try:
        promotion_type = PromotionType.objects.get(pk=int(request.data['type']))
        promotion = Promotion(user=request.user, type=promotion_type)
        promotion.save()
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def redeem_promotion(request):
    '''
    Log a promotion redeemed by a user, if the user has already redeemed it, don't redeem
    '''
    promotions = Promotion.objects.filter(user=request.user, type=int(request.data['type']), redeemed=False).order_by('-expiration')
    if promotions.count() == 0:
        # if user has not yet bought the promotion or there is no promotion type, do not redeem
        return Response(status=status.HTTP_403_FORBIDDEN)

    # set the first one to redeemed, we can implement multiple redemptions later
    serializer = PromotionSerializer(promotions[0], data={'redeemed': True}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

