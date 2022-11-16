from datetime import timedelta, date
from time import timezone
from events.models import Event
from weekly_digest.models import WeeklyDigestSubscription
from weekly_digest.serializers import WeeklyDigestSubscriptionSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader


class CreateWeeklyDigestSubscriptionView(CreateModelMixin, GenericAPIView):
    serializer_class = WeeklyDigestSubscriptionSerializer
    queryset = WeeklyDigestSubscription.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateWeeklyDigestSubscriptionView(RetrieveUpdateDestroyAPIView):
    queryset = WeeklyDigestSubscription.objects.all()
    serializer_class = WeeklyDigestSubscriptionSerializer


def trigger_digest_email(request):
    subscriptions = WeeklyDigestSubscription.objects.filter(subscribed=True).all()
    email_list = [s.email for s in subscriptions]
    events = digest_events()
    
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
            except BaseException as e:
                # Is there a better way to report errors?
                print('Email failed to send: ', e)

    try:
        return JsonResponse({ 'events': [e.event_name for e in events], 'users_count': len(email_list)}, safe=False)
    except BaseException as e:
        print('something went wrong')
        return JsonResponse({'message': str(e)}, status=400)

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
