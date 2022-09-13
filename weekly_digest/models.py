from django.db import models
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class WeeklyDigestSubscription(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    subscribed = models.BooleanField(default=False, blank=True, null=True)