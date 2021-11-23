from django.urls import path
from .views import AuthenticatedUser, login, logout, users, resister

urlpatterns = [
  path('users/', users),
  path('register/', resister),
  path('login/', login),
  path('logout/',logout),
  path('user/', AuthenticatedUser.as_view()),
  
]

