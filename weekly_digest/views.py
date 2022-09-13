from weekly_digest.models import WeeklyDigestSubscription
from weekly_digest.serializers import WeeklyDigestSubscriptionSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView

class CreateWeeklyDigestSubscriptionView(CreateModelMixin, GenericAPIView):
    serializer_class = WeeklyDigestSubscriptionSerializer
    queryset = WeeklyDigestSubscription.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateWeeklyDigestSubscriptionView(RetrieveUpdateDestroyAPIView):
    queryset = WeeklyDigestSubscription.objects.all()
    serializer_class = WeeklyDigestSubscriptionSerializer
