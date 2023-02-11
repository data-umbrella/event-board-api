from django.contrib import admin
from events.models import Event
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('author', 'created_at', 'updated_at')
    list_display = (
      "event_name",
      "start_date",
      "end_date",
      "featured",
      "published",
      "author",
      "review_link",
      "created_at",
      "updated_at",
    )

    def identifier(self, obj):
        return self.event_name


admin.site.register(Event, EventAdmin)
admin.site.site_header = 'Event Board API dashboard'
