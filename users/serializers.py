from dataclasses import field

import bcrypt
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserInfoSerializer(serializers.Serializer):
    user_info = serializers.CharField()
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()


class UserSignInSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True, max_length=255)

    def user_signin(self, data):

        user = User.objects.filter(email=data.get['email'])

        if not user or bcrypt.checkpw(data.get['password'], user.hashed_password):
            raise Response({"detail": "falied signin"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = self.get_token(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        data = {'user_info': user, 'refresh_token': refresh_token, 'access_token': access_token}
        serializer = UserInfoSerializer(data=data)
        serializer.is_valid()

        return serializer.data
