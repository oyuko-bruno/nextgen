from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)


    class Meta:
        swappable = "AUTH_USER_MODEL"

    # Inherit groups and user_permissions fields with custom related names
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), related_name='custom_user_permissions')
