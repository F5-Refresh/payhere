import re

import bcrypt
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSignUpSerializer(ModelSerializer):
    """
    date : 2022-07-05
    writer : 김동규
    """

    def create(self, validated_data):
        email = validated_data.get('email')
        nick_name = validated_data.get('nick_name')
        password = validated_data.get('hashed_password')

        # 패스워드 정규식표현(최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성/ 길이는 8~20자리)
        password_regexp = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'

        if not re.match(password_regexp, password):
            raise serializers.ValidationError({'password': ['유효한 패스워드를 입력하십시오.']})

        # 해싱된 패스워드
        hashed_password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')

        # 유저정보 DB 저장
        user = User.objects.create(email=email, nick_name=nick_name, hashed_password=hashed_password)

        return user

    class Meta:
        model = User
        fields = ['email', 'nick_name', 'hashed_password']
        extra_kwargs = {'hashed_password': {'write_only': True}}
