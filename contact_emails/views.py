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
        contact_email = 'learn@specollective.org'

        # TODO: add more params in body, test, and stretch goal to add template
        body = f"""
        name: {data['mame']}
        email: {data['email']}
        message: {data['message']}
        reference: {data['reference']}
        topic: {data['topicType']}
        """

        # NOTE: For this contact form we are sending the email to the sender.
        send_mail(
            'Contact Form Submission', #subject
            body, # body
            contact_email, #sender
            [contact_email], #recipient
            fail_silently=False,
        )

        # TODO: Determine what attributes we need to send to the client.
        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)