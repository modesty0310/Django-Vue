from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, serializers

from users.serializers import UserSerializer
from .models import User

@api_view(['POST'])
def resister(request):
  data = request.data

  if data['password'] != data['password_confirm']:
    raise exceptions.APIException('Password do not match')

  serializer = UserSerializer(data=data)
  serializer.is_valid(raise_exception=True)
  serializer.save()
  return Response(serializer.data)

@api_view(['POST'])
def login(request):
  email = request.data.get('email')
  password = request.data.get('password')

  user = User.objects.filter(email=email).first()

  if user is None:
    raise exceptions.AuthenticationFailed('존재하지 않는 이메일 입니다.')

  if not user.check_password(password):
    raise exceptions.AuthenticationFailed('비밀번호가 틀렸습니다.')

  return Response('로그인')

@api_view(['GET'])
def users(request):
  serializer = UserSerializer(User.objects.all(), many=True)
  return Response(serializer.data)


