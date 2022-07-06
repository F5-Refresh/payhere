import re

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.views import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    def create(self, validated_data):
        password = validated_data.get('password')

        # 패스워드 정규식표현(최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성/ 길이는 8~20자리)
        password_regexp = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'

        if not re.match(password_regexp, password):
            raise serializers.ValidationError({"password": ["올바른 비밀번호를 입력하세요."]})

        # 유저정보 DB 저장
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['email', 'nickname', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserInfoSerializer(serializers.Serializer):
    user_info = serializers.CharField()
    refresh = serializers.CharField()
    access = serializers.CharField()


class UserSignInSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True, max_length=255)

    def user_signin(self, data):
        user = User.objects.get(email=data['email'])
        if not user or not check_password(data['password'], user.password):
            raise_exception = exceptions.APIException(detail="failed signin")
            raise_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise raise_exception

        refresh = super().get_token(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        data = {'user_info': str(user), 'refresh': refresh_token, 'access': access_token}
        serializer = UserInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return serializer.data
