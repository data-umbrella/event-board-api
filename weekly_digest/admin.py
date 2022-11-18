from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from weekly_digest.utils import trigger_digest_email

from django.utils.safestring import mark_safe

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
      trigger_digest_email()
      return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_email/', self.send_email)
        ]
        return custom_urls + urls
    
    
admin.site.register(WeeklyDigestSubscription, WeeklyDigestSubscriptionAdmin)
