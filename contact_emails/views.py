import os
import json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response



@api_view(['GET', 'POST'])
def index(request):
    """
    API endpoint for sending contact emails.
    """
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        subject = 'Contact Form Submission'

        # TODO: Enforce snake case for topicType on client side.
        body = f"""
        name: {data['name']}
        email: {data['email']}
        message: {data['message']}
        reference: {data['reference']}
        topic: {data['topicType']}
        """

        # NOTE: For this contact form we are sending the email to the sender.
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER, #sender
            [settings.EMAIL_HOST_USER], #recipient
            fail_silently=False,
        )

        # TODO: Determine what attributes we need to send to the client.
        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)