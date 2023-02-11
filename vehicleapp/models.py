from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Super Admin'),
        (2, 'Admin'),
        (3, 'User'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=3)


class Vehicle(models.Model):
    
    
    VEHICLE_TYPE=(
        ('two wheeler','Two Wheeler'),
        ('three wheeler','Three Wheeler'),
        ('four wheeler','Four Wheeler')
    )
    
    alphanumeric=RegexValidator(r"^[0-9a-zA-Z_]*$",'Only use alphanumeric characters')
    

    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    vnumber=models.CharField(max_length=50,validators=[alphanumeric])
    vtype=models.CharField(choices=VEHICLE_TYPE,default='Two Wheeler',max_length=50)
    vmodel=models.TextField(max_length=50)
    vdescription=models.TextField(max_length=100)
    
    