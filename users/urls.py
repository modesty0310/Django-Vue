from django.urls import path
from .views import users, resister

urlpatterns = [
  path('users/', users),
  path('register/', resister)
]

