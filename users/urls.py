from django.urls import path
from .views import AuthenticatedUser, login, users, resister

urlpatterns = [
  path('users/', users),
  path('register/', resister),
  path('login/', login),
  path('user/', AuthenticatedUser.as_view())
]

