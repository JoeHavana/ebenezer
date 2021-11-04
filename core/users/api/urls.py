from django.urls import path
from core.users.api.views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = "users"

urlpatterns = [
    path('register/', registration_view, name="register"),
    path('login/', obtain_auth_token, name="login"),

    path('users/', users_list_api_view, name="all-user"),
    path('user/<int:pk>/', user_detail_api_view, name="get-user"),
    path('user/<int:pk>/update/', update_user, name="update-user"),
]
