from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser

class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    info = models.TextField()

class CustomUser(AbstractUser):
    # fields and other definitions
    is_editor = models.BooleanField(default=False)

    def has_edit_permission(self):
        return self.is_editor
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_users'  # Add a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='custom_users'  # Add a unique related_name
    )

