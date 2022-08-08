from django.urls import path

from . import views

urlpatterns = [
    path('contact_emails', views.index, name='index'),
]