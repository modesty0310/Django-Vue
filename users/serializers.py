from rest_framework import fields, serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'email', 'password']
    extra_kwargs = {
      'password' : {'write_only' : True} # 사용자 정보를 불러올 떄 비밀번호는 빼고 가저온다.
    }