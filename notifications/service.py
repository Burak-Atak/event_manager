from django.db.models import QuerySet

from notifications.models import Notification


class NotificationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NotificationService, cls).__new__(cls)
        return cls._instance

    def create_notification(self, data):
        return Notification.objects.create(**data)

    def update_notification(self, notification: Notification, data):
        for attr, value in data.items():
            setattr(notification, attr, value)

        notification.save()

        return notification

    def bulk_update_notifications_by_queryset(self, notifications: QuerySet, data):
        notifications.update(**data)

    def bulk_update_notifications(self, notifications: list, fields):
        Notification.objects.bulk_update(notifications, fields, batch_size=1000)


class NotificationLogService:
    pass
