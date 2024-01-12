from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    bio = models.CharField(max_length=255,null=True,blank=True)
    avatar = models.ImageField(null=True,blank=True)