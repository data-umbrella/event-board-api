import os

from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes


def get_token_from_request(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    cookie_token = request.COOKIES.get('access_token')

    if cookie_token: return cookie_token
    if auth_header: return auth_header.split()[1]

    return None


def get_user_from_token(token):
    if token is None: return None

    try:
      return Token.objects.get(key=token).user
    except Token.DoesNotExist:
      return None


def render_success_response(token, user):
    # Initial response object
    response = Response()

    # Set response status
    response.status = status.HTTP_201_CREATED

    # Set HTTP headers
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    # Set HTTP only cookies
    response.set_cookie(
        'access_token',
        value=token,
        max_age=(3600 * 24 * 14),
        expires=None,
        httponly=True,
        samesite='None',
        domain=settings.AUTH_COOKIE_DOMAIN,
        secure=True,
    )

    # Set response data
    response.data = {
        'email': user.email,
        'is_staff': user.is_staff,
        'id': user.id,
        'email_verified': user.email_verified,
    }

    # Return final response
    return response


def render_error_response():
    return Response({ 'message': 'something went wrong' }, status=status.HTTP_401_UNAUTHORIZED)


class CurrentUserView(ObtainAuthToken):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = get_token_from_request(request)
        user = get_user_from_token(token)

        if user is None:
            return render_error_response()
        else:
            return render_success_response(token, user)


# DELETE /api/sign_out
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def sign_out(request):
    """
    API endpoint to logout a current user
    """
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.set_cookie(
        'access_token',
        value='',
        expires=None,
        httponly=True,
        samesite='None',
        domain=settings.AUTH_COOKIE_DOMAIN,
        secure=True,
    )
    return response
