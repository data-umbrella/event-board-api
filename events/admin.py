from django.contrib import admin
from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
      "id",
      "title",
      "organization_name",
      "start_date",
      "end_date",
    )

    def identifier(self, obj):
        return obj.id


admin.site.register(Event, EventAdmin)
