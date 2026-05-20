from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('البريد الإلكتروني مطلوب')
        email = self.normalize_email(email)
        user  = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role',         'admin')
        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('guest',  'Guest'),
        ('user',   'User'),
        ('expert', 'Expert'),
        ('admin',  'Admin'),
    ]

    email       = models.EmailField(unique=True)
    full_name   = models.CharField(max_length=150)
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    avatar      = models.ImageField(upload_to='avatars/', null=True, blank=True)
    device_id   = models.CharField(max_length=255, blank=True)  # للـ Guest
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']

    @property
    def role_level(self):
        levels = {
            'guest':  0,
            'user':   1,
            'expert': 2,
            'admin':  3,
        }
        return levels.get(self.role, 0)

    @property
    def is_expert(self):
        return self.role in ['expert', 'admin']

    @property
    def is_admin_role(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.full_name} ({self.role})"