from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions, viewsets
from rest_framework.views import APIView

from .authentication import generate_acess_token, JWTAuthentication
from .serializers import PermissionSerializer, RoleSerializer, UserSerializer
from .models import Role, User, Permission

@api_view(['POST'])
def resister(request):
  """
  회원가입
  1. email은 unique로 지정 해둠
  2. 비밀번호가 일치 하는지 확인
  3. userserializer 생성
  4. is_vaild() 유효한지 확인
  5. 저장
  """
  data = request.data

  if data['password'] != data['password_confirm']:
    raise exceptions.APIException('Password do not match')

  serializer = UserSerializer(data=data)
  serializer.is_valid(raise_exception=True)
  serializer.save()
  return Response(serializer.data)

@api_view(['POST'])
def login(request):
  """
  로그인
  1. email 확인
  2. 비밀번호 확인
  3. 로그인 후 jwt 발행
  """
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
  """
  로그아웃
  1. delete_cookie
  2. 성공문자 리턴
  """
  response = Response()
  response.delete_cookie(key='jwt')
  response.data = {
    'message': 'success'
  }

  return response


class AuthenticatedUser(APIView):
  """
  유저 확인
  1. authentication_classes설정 custom Authentication으로 확인
  2. serializer 생성
  """
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)

    return Response({
      'data' : serializer.data
    })


class PermissionAPIView(APIView):
  """
  권한 확인
  1. authentication_classes설정 custom Authentication으로 확인
  2. serializer 생성
  """
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = PermissionSerializer(Permission.objects.all(), many=True)

    return Response({
      'data' : serializer.data
    })

class RoleViewSet(viewsets.ViewSet):
  """
  Role 확인
  1. list 모든 유저의 role를 보여줌
  """
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def list(self, request):
    serializer = RoleSerializer(Role.objects.all(), many=True)

    return Response({
      'data':serializer.data
    })

  def create(self, request):
    pass

  def retrieve(self, request, pk=None):
    pass

  def update(self, request, pk=None):
    pass

  def destroy(self, request, pk=None):
    pass
