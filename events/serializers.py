from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Event
