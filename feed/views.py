from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from feed.models import Venue, District
from feed.serializers import VenueSerializer, DistrictSerializer
from user_post.models import Post
from user_post.serializers import PostSerializer
from django.db.models import Count

class VenueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows venues to be viewed or edited.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows districts to be viewed or edited.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


# @list_route(methods=['get'])
@api_view(['GET'])
def get_district_feed(request, pk):
    venues = Venue.objects.filter(district=pk
        ).annotate(post_count=Count("post")
        ).order_by('-post_count')
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bar_feed(request, pk):
    posts = Post.objects.filter(venue=pk
        ).annotate(like_count=Count("like")
        ).order_by('-like_count'
        ).exclude(like_count=0)
    # for testing purposes I exclude posts without likes
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_highlights_feed(request, pk):
    posts = Post.objects.filter(venue__district=pk
        ).annotate(like_count=Count("like")
        ).order_by('-like_count'
        ).exclude(like_count=0)
    # for testing purposes I exclude posts without likes
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)