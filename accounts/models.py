from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for User model without username
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove username

    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('SUPER_ADMIN', 'Super Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    LOCATION_CHOICES = (
        ('HYDERABAD', 'Hyderabad'),
        ('DELHI', 'Delhi'),
        ('MUMBAI', 'Mumbai'),
    )
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)

    lead = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'ADMIN'}
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # IMPORTANT

    def __str__(self):
        return self.email