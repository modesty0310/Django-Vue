from django.urls import path
from .views import login, users, resister

urlpatterns = [
  path('users/', users),
  path('register/', resister),
  path('login/', login)
]

