from django.db import models
from user.models import User
import random

class Otp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.IntegerField(max_length=6,blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp



