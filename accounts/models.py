from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Phone field must be set')
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, name, password, **extra_fields)



class CustomUser(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(unique=True)
    # phone=models.IntegerField(unique=True,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # otp=models.CharField(max_length=6,null=True,blank=True)
    # otp_expiration = models.DateTimeField(null=True,blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email
    

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True,unique=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    tab_url = models.URLField(null=True, blank=True)
    options=(
        ('CyberPark','CyberPark'),
        ('InfoPark','InfoPark'),
        ('TechnoPark','TechnoPark')
    )
    park=models.CharField(max_length=100,choices=options,default="CyberPark")
    def __str__(self):
        return self.name