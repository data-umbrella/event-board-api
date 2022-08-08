from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json


@api_view(['GET', 'POST'])
def index(request):
    """
    API endpoint for sending contact emails.
    """
    if request.method == 'GET':
        return Response({'ping': 'pong'})
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # TODO: parse other parameters
        email = data['email']

        # TODO: Implement logic to send email

        # TODO: Determine what attributes we need to send to the client.
        return Response({'email': email}, status=status.HTTP_201_CREATED)