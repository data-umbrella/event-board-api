import os
import json
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['DELETE'])

def delete_user(request, email):
  """
    API endpoint for deleting user account
  """
#   User = get_user_model()
  user = User.objects.get(email=email)
  if request.method == 'DELETE':
    user.delete()
    return JsonResponse({'message': 'User deleted successfully.'}, status=204)
  else:
      return HttpResponse(status=405)

# return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)
#does this need to be organized as a class? class UserViewSet(viewsets.ModelViewSet):


