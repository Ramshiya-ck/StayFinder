from django.db import models
from django.contrib.auth.models import AbstractUser

from user.manager import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=256, error_messages={'unique':'email already exist'})
    is_customer = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'Users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']

        def __str__(self):
            return self.email
            
    









