from django.db import models
from user.models import User
import random


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    id_proof = models.CharField(max_length=100, blank=True, null=True)  
    nationality = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.user.email



    




