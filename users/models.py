from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        PROVIDER = 'PROVIDER', 'Service Provider'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, choices=UserType.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    experienceInfo = models.TextField(blank=True, default='')
    idProof = models.ImageField(upload_to='id-proofs/', blank=True, null=True)
    isVerified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Provider: {self.user.email}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        return f'Customer: {self.user.email}'
