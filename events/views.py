from rest_framework import generics, mixins
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ListEvent(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [
      IsAuthenticatedOrReadOnly
    ]
    filter_backends = [
      SearchFilter,
      DjangoFilterBackend
    ]
    search_fields = [
        'title',
        'description',
    ]
    filterset_fields = ['featured']


class DetailEvent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
