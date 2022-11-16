from django.core.mail import send_mail
from django.conf import settings


def weekly_digest_job(self, *args, **options):
    subscribed_users = WeeklyDigestSubscription.objects.filter(
        subscribed=True
    ).all()

    send_mail(
        'subject',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['daniel.ashcraft@gmail.com'],
        fail_silently=False,
    )
    print('Successfully sent')
