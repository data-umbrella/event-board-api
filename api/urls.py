from django.urls import path
from .views import ListEvent, DetailEvent

urlpatterns = [
    path('events', ListEvent.as_view()),
    path('events/<int:pk>/', DetailEvent.as_view()),
]
