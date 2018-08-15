from django.contrib.auth.hashers import make_password,check_password
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='用户名'
    )
    password = models.CharField(
        max_length=100,
        verbose_name='密码'
    )
    email = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='邮箱'
    )
    photo = models.CharField(
        max_length=100,
        verbose_name='头像',
        blank=True,
        null=True
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.password = make_password(self.password)
        super().save()

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name