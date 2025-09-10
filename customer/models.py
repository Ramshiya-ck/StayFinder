from django.db import models
from user.models import User
import random


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(blank=True,null=True)
    profile_image = models.FileField(upload_to='profile_images',blank=True,null=True)
    

    def __str__(self):
        return self.user.email



    




