# import logging
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from rest_framework.authtoken.models import Token
from drfpasswordless.models import CallbackToken
from drfpasswordless.settings import api_settings

def inject_template_context(context):
    """
    Injects additional context into email template.
    """
    for processor in api_settings.PASSWORDLESS_CONTEXT_PROCESSORS:
        context.update(processor())
    return context

def send_email_with_callback_token(user, email_token, **kwargs):
    """
    Sends a Email to user.email.
    Passes silently without sending in test environment
    """

    try:
        # Make sure we have a sending address before sending.

        # Get email subject and message
        email_subject = kwargs.get('email_subject',
                                    api_settings.PASSWORDLESS_EMAIL_SUBJECT)
        email_plaintext = kwargs.get('email_plaintext',
                                        api_settings.PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE)
        email_html = kwargs.get('email_html',
                                api_settings.PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME)

        # Inject context if user specifies.
        context = inject_template_context({
            'callback_token': email_token.key,
            'email': user.email,
        })
        html_message = loader.render_to_string(email_html, context,)
        send_mail(
            email_subject,
            email_plaintext % email_token.key,
            api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS,
            [getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME)],
            fail_silently=False,
            html_message=html_message,)
        return True
    except Exception as e:
        # TODO: Add back logging via logger
        # logger.debug("Failed to send token email to user: %d."
        #   "Possibly no email on user object. Email entered was %s" %
        #   (user.id, getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME)))
        # logger.debug(e)
        print(e)
        return False
