from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Handles creating users with email instead of username"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize email format
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password for security
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create an admin user (superuser)"""
        extra_fields.setdefault("is_staff", True)  # Can access admin panel
        extra_fields.setdefault("is_superuser", True)  # Has all permissions
        extra_fields.setdefault("email_verified", True)  # Superusers bypass email verification
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model that uses email for login instead of username"""

    username = None  # Remove username field
    email = models.EmailField(unique=True)  # Email is unique and required
    first_name = models.CharField(max_length=150, blank=False)  # Required
    last_name = models.CharField(max_length=150, blank=True)  # Optional
    phone = models.CharField(max_length=15, blank=True)  # Optional phone number
    address = models.TextField(blank=True)  # Full address
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Email verification fields
    email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)

    USERNAME_FIELD = "email"  # Use email for login
    REQUIRED_FIELDS = ["first_name"]  # Required when creating superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email  # Display email when printing user object
