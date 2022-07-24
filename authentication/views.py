import os
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins


DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', 'False') == 'True'
PROD_COOKIE_DOMAIN = os.environ.get('PROD_COOKIE_DOMAIN', '')
AUTH_COOKIE_DOMAIN = 'localhost' if DEVELOPMENT_MODE else PROD_COOKIE_DOMAIN


class CurrentUserView(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        auth_header = request.META['HTTP_AUTHORIZATION']
        cookie_token = request.COOKIES.get('TOKEN')

        if cookie_token:
            token = cookie_token
        else:
            token = auth_header.split()[1]

        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response({ 'message': 'error' }, status=401)

        response = Response({
            'email': user.email,
            'is_staff': user.is_staff,
        }, status=200)

        response.set_cookie(
            'access_token',
            value=token,
            max_age=(3600 * 24 * 14),
            expires=None,
            httponly=True,
            samesite='None',
            domain='localhost',
            secure=True,
        )

        return response
