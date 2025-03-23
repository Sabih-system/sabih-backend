# api/urls.py
from django.urls import path
from .views import UsersideRequestAPI

urlpatterns = [
    path('submit-request/', UsersideRequestAPI.as_view(), name='submit-request'),
]
