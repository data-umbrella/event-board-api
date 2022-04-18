from rest_framework import serializers
from events import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'featured',
        )
        model = models.Event
