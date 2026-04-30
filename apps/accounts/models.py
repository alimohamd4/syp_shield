from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('البريد الإلكتروني مطلوب')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    TIER_CHOICES = [
        ('standard', 'Standard'),
        ('gold', 'Gold'),
        ('obsidian', 'Obsidian'),
    ]

    email      = models.EmailField(unique=True)
    full_name  = models.CharField(max_length=150)
    tier       = models.CharField(max_length=20, choices=TIER_CHOICES, default='standard')
    avatar     = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']

    @property
    def tier_level(self):
        levels = {'standard': 1, 'gold': 2, 'obsidian': 3}
        return levels.get(self.tier, 1)

    def __str__(self):
        return f"{self.full_name} ({self.tier})"