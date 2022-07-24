from rest_framework import serializers
from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'featured',
            'hash_tag',
            'conference_name',
            'organization_name',
            'acronym',
            'event_url',
            'organization_url',
            'startDate',
            'endDate',
            'startTime',
            'endtime',
            'location',
            'region',
            'in_person',
            'virtual',
            'cfp_due_date',
            'language',
            'code_of_conduct_url',
        )
        model = models.Event
