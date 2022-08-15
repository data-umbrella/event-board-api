from django.contrib import admin
from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
      "event_name",
      "organization_name",
      "start_date",
      "end_date",
    )

    def identifier(self, obj):
        return self.event_name


admin.site.register(Event, EventAdmin)
