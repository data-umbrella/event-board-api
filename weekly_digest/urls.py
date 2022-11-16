from django.urls import path
from weekly_digest.views import (
  CreateWeeklyDigestSubscriptionView,
  UpdateWeeklyDigestSubscriptionView,
  trigger_digest_email,
)

urlpatterns = [
    path('weekly_digests', CreateWeeklyDigestSubscriptionView.as_view()),
    path('weekly_digests/<int:pk>/', UpdateWeeklyDigestSubscriptionView.as_view()),
    path('trigger_weekly_digests', trigger_digest_email),
]
