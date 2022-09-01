from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.mail import send_mail


@api_view(['GET', 'POST'])
def index(request):
    """
    API endpoint for sending contact emails.
    """
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # TODO: parse other parameters
        email = data['email']
        message = data['message']
        # TO DO: add more params in body, test, and stretch goal to add template
        body = f"""
            message: {message}
            
            """

        send_mail(
            'Contact Form Submission', #subject
            message, #body
            'learn@specollective.org', #sender
            [email], #recipient
            fail_silently=False,
        )

        # TODO: Implement logic to send email

        # TODO: Determine what attributes we need to send to the client.
        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)