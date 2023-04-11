from django.urls import path
from .views import CurrentUserView, sign_out, delete_account

urlpatterns = [
    path('current_user/', CurrentUserView.as_view()),
    path('sign_out/', sign_out, name='sign_out'),
    path('delete_account/', delete_account, name='delete_account'),
]
