from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    account = models.CharField(max_length=10, verbose_name='账号名')
    telephone = models.CharField(max_length=11, verbose_name="手机号")
    head = models.ImageField(verbose_name="头像", upload_to="heads/", default="/heads/default.png")
