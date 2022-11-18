from datetime import timedelta, date
from time import timezone
from events.models import Event
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader

from weekly_digest.models import WeeklyDigestSubscription

def trigger_digest_email():
    # Import helper method to make running from the console easier, only having to import trigger_digest_email
    # TODO: remove once email is triggered by admin controls and/or a cron job
    from weekly_digest.utils import digest_events
    
    subscriptions = WeeklyDigestSubscription.objects.filter(subscribed=True).all()
    email_list = [s.email for s in subscriptions]
    events = digest_events()
    
    html_message = loader.render_to_string('emails/weekly_digest_events.html', {'events': events})

    if len(events) > 0:
        for email in email_list:
            try:
                email_subject = 'Weekly Digest'
                email_plaintext = 'Weekly Digest'
                html_message = loader.render_to_string('emails/weekly_digest_events.html', {'events': events})

                send_mail(
                    email_subject,
                    email_plaintext,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=html_message,)
                return True
            except BaseException as e:
                print('Email failed to send: ', e)
                return False


def digest_events():
    try:
        # get events happening in next 7 days
        today = date.today().strftime("%Y-%m-%d")
        next_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        next_month = (date.today() + timedelta(days=28)).strftime("%Y-%m-%d")

        events = Event.objects.filter(start_date__range=[today, next_week]).all()

        # get events happening in next 28 days
        if len(events) == 0:
            events = Event.objects.filter(start_date__range=[today, next_month]).all()
        
        return events

    except BaseException as e:
        print('No events found', e)
        return []
