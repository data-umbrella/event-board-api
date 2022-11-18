from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from weekly_digest.utils import trigger_digest_email
from django.contrib import messages

from weekly_digest.models import WeeklyDigestSubscription

class WeeklyDigestSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
      'email',
      'subscribed',
    )

    list_filter = ('email', 'subscribed')

    change_list_template = 'admin/weekly_digests/weekly_digests_change_list.html'
    
    def identifier(self, _obj):
      return self.email

    def send_email(self, request):
      email_sent = trigger_digest_email()
      if (email_sent):
          self.message_user(request, "✨ The Weekly Digest email was successfully sent to all subscribers!")
      else:
          messages.error(request, "The Weekly Digest email failed to send")

      return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_email/', self.send_email)
        ]
        return custom_urls + urls
    
    
admin.site.register(WeeklyDigestSubscription, WeeklyDigestSubscriptionAdmin)
