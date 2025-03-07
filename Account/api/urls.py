from django.urls import path
from .views import *

urlpatterns = [
    path('login/', main_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('csrf_token/', csrf_token_view, name='csrf_token'),
    path('get_user/', get_logged_in_user ,name ="get_user"),
    path('register/', UserRegistrationView.as_view(), name='register'),
]