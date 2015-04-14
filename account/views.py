from datetime import datetime, timedelta
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from social.apps.django_app.utils import psa
from account.serializers import UserSerializer
from rest_framework.response import Response
from promotion.models import Promotion
from promotion.serializers import PromotionSerializer
from user_post.models import Post, Like
from user_post.serializers import PostSerializer, LikeSerializer, ExtendedPostSerializer
from user_post.views import formatted_time_proximity


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@psa()
def auth_by_token(request, backend):
    user = request.user
    user = request.backend.do_auth(
        access_token=request.DATA.get('access_token'),
        user=user.is_authenticated() and user or None
    )
    if user and user.is_active:
        login(request, user)
        return user
    else:
        return None


@csrf_exempt
@api_view(['POST'])
def social_register(request):
    user = auth_by_token(request, "facebook")  # hard coded facebook because that's all we plan to support atm
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_users_feed(request):
    """
    Returns a list of all users ordered by private key
    """
    promotions = User.objects.all().order_by('-pk')
    serializer = UserSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_limited_users_feed(request, limit):
    """
    Returns a list of users of size limit, ordered by private key
    """
    if limit > 0:
        promotions = User.objects.all().order_by('-pk')
        serializer = UserSerializer(promotions[:limit], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return get_users_feed(request)


@csrf_exempt
@api_view(['GET'])
def get_recent_user_posts(request, user):
    """
    Returns a list of all posts made by a user, newest first
    """
    posts = Post.objects.filter(user=user).annotate(Count("like")).order_by('-timestamp')
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    serializer = ExtendedPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_top_user_posts(request, user):
    """
    Returns a list of all posts made by a user, most likes first
    """
    posts = Post.objects.filter(user=user).annotate(Count("like")).order_by('-like__count')
    serializer = ExtendedPostSerializer(posts, many=True)
    for post in posts:
        post.time_text = formatted_time_proximity(post.timestamp)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_user_likes(request, user):
    """
    Returns a list of all posts liked by a user
    """
    likes = Like.objects.filter(user=user).annotate(Count("post")).order_by('-post__count')
    serializer = LikeSerializer(likes, many=True)
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
def get_user_redeemed_promotion_feed(request, pk):
    """
    Returns a list of all unredeemed promotions "purchased" by a particular user

    e.g. input user ID, get back promotions about free cover and discounts that have not yet been redeemed
    """
    promotions = Promotion.objects.filter(user=pk, redeemed=True).order_by('-expiration')
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
