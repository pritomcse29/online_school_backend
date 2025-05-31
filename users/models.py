from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    # choices_fields =(
    #  ("ADMIN","Admin"),
    #  ("TEACHER","Teacher"),
    #  ("STUDENT","Student"),
    # )
        
   
    username = None
    email = models.EmailField(unique=True,max_length=50)
    address =  models.CharField(max_length=100, blank=True,null=True)
    number = models.IntegerField(null=True,blank=True)
    # role = models.CharField( max_length=20,default="student")
    # role = models.CharField( max_length=20,choices= choices_fields,default="STUDENT")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    # def save(self, *args, **kwargs):
    #     if self.role=="admin" and not self.is_staff:
    #         raise ValueError ("Only admin can add admin")
    #     super().save(*args, **kwargs)
    
