from rest_framework import generics, mixins
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class ListEvent(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
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
        'event_name',
        'organization_name',
        'description',
        'tags',
    ]
    filterset_fields = {
        'featured': ['exact'],
        'start_date':['gte', 'lte', 'exact', 'gt', 'lt'],
    }


class DetailEvent(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        # print(self)
        # image_file = request.data['image_file']
        # request.data['image_file'] = None
        #
        try:
            # instance = self.get_object()
            # # instance.image_file = image_file
            # instance.save()
            return self.update(request, *args, **kwargs)
        except BaseException as e:
            print('something went wrong')
            return Response({'message': str(e)}, status=400)
