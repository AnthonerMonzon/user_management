from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    """
    class UserType(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'SuperAdmin'
        EDITOR = 'EDITOR', 'Editor'

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.EDITOR
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_superadmin(self):
        return self.user_type == self.UserType.SUPERADMIN

    def is_editor(self):
        return self.user_type == self.UserType.EDITOR

    def can_manage_users(self):
        """Only SuperAdmin can manage users"""
        return self.user_type == self.UserType.SUPERADMIN

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
