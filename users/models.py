from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    settings = models.JSONField(default=dict, serialize=False)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_notifications_active(self):
        default_notification_is_active = settings.DEFAULT_USER_SETTINGS.get(
            'notification_settings', {}).get('is_active')

        return self.settings.get(
            'notification_settings', {}).get('is_active', default_notification_is_active)
