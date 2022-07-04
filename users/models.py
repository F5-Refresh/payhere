from core.models import TimeStamp as TimeStampModel
from django.db import models


# Create your models here.
class User(TimeStampModel):
    hashed_password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nick_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'이메일: {self.email} / 닉네임: {self.nick_name}'
