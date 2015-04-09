from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from social.apps.django_app.utils import load_backend, psa, strategy
from account.serializers import UserSerializer
from social.apps.django_app import load_strategy
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@strategy()
def auth_by_token(request, backend):
    user = request.user
    user = request.backend.do_auth(
        access_token=request.DATA.get('access_token'),
        user=user.is_authenticated() and user or None
    )
    if user and user.is_active:
        return user
    else:
        return None


@csrf_exempt
@api_view(['POST'])
def social_register(request):
    auth_token = request.DATA.get('access_token', None)
    if auth_token:
        try:
            user = auth_by_token(request, "facebook")
        except Exception, err:
            return Response(str(err), status=400)
        if user:
            login(request, user)
            return Response("User logged in", status=status.HTTP_200_OK)
        else:
            return Response("Bad Credentials", status=403)
    else:
        return Response("Bad request", status=400)

