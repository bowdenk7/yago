from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from social.apps.django_app.utils import strategy, psa
from account.serializers import UserSerializer
from rest_framework.response import Response


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