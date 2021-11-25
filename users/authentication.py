import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

def generate_acess_token(user):
  """
  jwt 토큰 생성
  1. payload 생성 (user_id, 만료일, 생성시간)
  2. jwt encode 후 리턴
  """
  payload = {
    'user_id': user.id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    'iat': datetime.datetime.utcnow()
  }

  return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class JWTAuthentication(BaseAuthentication):
  """
  jwt 확인
  1. BaseAuthentication 상속
  2. def authenticate
  3. jwt 가져오기
  4. 토큰 비었는지 확인
  5. jwt decode
  6. user 정보 가져오기
  7. user 정보 리턴
  """
  def authenticate(self, request):
    token = request.COOKIES.get('jwt')

    if not token: 
      return None

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise exceptions.AuthenticationFailed('unauthenticated')

    user = get_user_model().objects.filter(id=payload['user_id']).first()

    if user is None:
      raise exceptions.AuthenticationFailed('user not found')
    
    return  (user, None)