from django.db import models
from user.models import User
import random


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email



    




