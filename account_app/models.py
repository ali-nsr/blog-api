from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


# Create your models here.

class User(AbstractBaseUser):
    """
    user class for creating users with email and password
    """
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # fields required for admin
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='user-images', null=True, blank=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
