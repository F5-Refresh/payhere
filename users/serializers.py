import re

import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions, serializers
from rest_framework.views import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


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
