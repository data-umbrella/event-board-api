from django.contrib import admin
from events.models import Event
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe


class EventAdmin(admin.ModelAdmin):
    list_display = (
      "event_name",
      "start_date",
      "featured",
      "published",
      "author",
      "review_link",
    )
    readonly_fields = ('author',)

    def identifier(self, obj):
        return self.event_name


admin.site.register(Event, EventAdmin)
