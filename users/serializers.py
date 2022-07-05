import re

import bcrypt
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    def create(self, validated_data):
        email = validated_data.get('email')
        nick_name = validated_data.get('nick_name')
        password = validated_data.get('hashed_password')

        password_regexp = '\S{8,20}$'

        if not re.match(password_regexp, password):
            raise serializers.ValidationError({'password': ['유효한 패스워드를 입력하십시오.']})

        hashed_password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        user = User.objects.create(email=email, nick_name=nick_name, hashed_password=hashed_password)

        return user

    class Meta:
        model = User
        fields = ['email', 'nick_name', 'hashed_password']
        extra_kwargs = {'hashed_password': {'write_only': True}}
