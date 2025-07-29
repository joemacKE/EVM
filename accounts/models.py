from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You must provide valid email (example@gmail.com)")

        user = self.model(
            email = self.nomralize_email(email),
            password = password
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    
    def create_superuser(self, email, password=None, **extrafields):
        if not email:
            raise ValueError("You must provide a valid email (example@gmail.com)")
        user = self.create_user(
            email = email,
            password = password
        )
        user.is_admin - True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class CustomUser(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile/') #must check this later

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()


    def __str__(self):
        return f"{self.first_name} {self.email}"

    ...

# Create your models here.
