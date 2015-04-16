from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from feed.models import Venue
from promotion.models import PromotionType, Promotion
from promotion.serializers import PromotionTypeSerializer, PromotionSerializer, PromotionFeedSerializer
from django.core.exceptions import ObjectDoesNotExist


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
    for promotion in promotions:
        promotion.venue_name = Venue.objects.get(pk=promotion.venue.pk).name
    serializer = PromotionFeedSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_venue_promotion_type_feed(request, pk):
    """
    Returns a list of all promotions for a particular venue

    e.g. input Red Door, get back promotions about free cover and discounts at Red Door
    """
    promotions = PromotionType.objects.filter(venue=pk).order_by('-point_cost')
    for promotion in promotions:
        promotion.venue_name = Venue.objects.get(pk=promotion.venue.pk).name
    serializer = PromotionFeedSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_district_promotion_type_feed(request, pk):
    """
    Returns a list of all promotions for a particular district

    e.g. input Buckhead, get back promotions about free cover and discounts at Red Door, Moondogs, etc.
    """
    promotions = PromotionType.objects.filter(venue__district=pk).order_by('-point_cost')
    for promotion in promotions:
        promotion.venue_name = Venue.objects.get(pk=promotion.venue.pk).name
    serializer = PromotionFeedSerializer(promotions, many=True)
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
        request.user.current_points -= promotion_type.point_cost
        request.user.save()
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST'])
def purchase_and_redeem(request):
    '''
    Creates a promotion and redeems it immedietly. Removes points from user. Returns user's new balance.
    '''
    try:
        promotion_type = PromotionType.objects.get(pk=int(request.data['type']))
        promotion = Promotion(user=request.user, type=promotion_type, redeemed=True)
        promotion.save()
        request.user.current_points -= promotion_type.point_cost
        request.user.save()
        return Response({"new_points_total": request.user.current_points}, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)