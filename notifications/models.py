from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from enumfields import EnumField

from notifications.enums import NotificationTypeEnum, NotificationStatus


class Notification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    trigger_date = models.DateTimeField(db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True,
                             related_name='notifications')
    is_active = models.BooleanField(default=True)
    is_broadcast = models.BooleanField(
        default=False)  # TODO: Future feature to send notifications to all allowed users

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id'])
        ]


class NotificationLog(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(choices=NotificationTypeEnum.choices, max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[choice for choice in NotificationStatus.choices()]
    )
    created_date = models.DateTimeField(auto_now_add=True)
