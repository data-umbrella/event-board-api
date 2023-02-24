from django.urls import path
from .views import CurrentUserView, sign_out

urlpatterns = [
    path('current_user/', CurrentUserView.as_view()),
    path('sign_out/', sign_out, name='sign_out'),
    path('update_user_email/', UpdateUserEmail.as_view(), name='update_user_email'),
   
]
