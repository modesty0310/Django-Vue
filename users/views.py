from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions, viewsets
from rest_framework.views import APIView

from .authentication import generate_acess_token, JWTAuthentication
from .serializers import PermissionSerializer, UserSerializer
from .models import User, Permission

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

  response = Response()

  token = generate_acess_token(user)
  response.set_cookie(key='jwt', value=token, httponly=True)
  response.data = {
    'jwt': token
  }

  return response

@api_view(['POST'])
def logout(request):

  response = Response()
  response.delete_cookie(key='jwt')
  response.data = {
    'message': 'success'
  }

  return response


class AuthenticatedUser(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)

    return Response({
      'data' : serializer.data
    })


class PermissionAPIView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = PermissionSerializer(Permission.objects.all(), many=True)

    return Response({
      'data' : serializer.data
    })

class RoleViewSet(viewsets.ViewSet):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def list(self, request):
    pass

  def create(self, request):
    pass

  def retrieve(self, request, pk=None):
    pass

  def update(self, request, pk=None):
    pass

  def destroy(self, request, pk=None):
    pass
