from rest_framework import serializers
from weekly_digest.models import WeeklyDigestSubscription


class WeeklyDigestSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WeeklyDigestSubscription
