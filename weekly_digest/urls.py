from django.urls import path
from weekly_digest.views import (
  CreateWeeklyDigestSubscriptionView,
  UpdateWeeklyDigestSubscriptionView,
)

urlpatterns = [
    path('weekly_digests', CreateWeeklyDigestSubscriptionView.as_view()),
    path('weekly_digests/<int:pk>/', UpdateWeeklyDigestSubscriptionView.as_view()),
]
