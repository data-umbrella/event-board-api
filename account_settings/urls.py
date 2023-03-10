from django.urls import path
from . import views

urlpatterns = [
    path('delete_user_account', views.delete_user, name='email'),
]