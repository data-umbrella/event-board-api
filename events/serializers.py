from rest_framework import serializers
from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'accessibility_options',
            'acronym',
            'cfp_due_date',
            'code_of_conduct_url',
            'conference_name',
            'description',
            'end_date',
            'end_time',
            'event_notes',
            'event_type',
            'event_url',
            'featured',
            'hash_tag',
            'id',
            'in_person',
            'language',
            'location',
            'organization_name',
            'organization_url',
            'region',
            'start_date',
            'start_time',
            'title',
            'virtual',
            'volunteering_notes',
            'tags',
        )
        model = models.Event
