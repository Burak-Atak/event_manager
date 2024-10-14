from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from recurrence.fields import RecurrenceField
from notifications.models import Notification
from notifications.service import NotificationService


class StarterModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class NotifiableModel(models.Model):
    recurrence = RecurrenceField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    is_recurrence = models.BooleanField(default=False)
    is_notifications_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_recurrence and not self.recurrence:
            raise ValueError("Recurrence field is required if is_recurrence is True")

        if self.recurrence:
            self.recurrence.dtstart = self.start_date
            if self.recurrence.dtend and self.recurrence.dtend < self.start_date:
                self.recurrence.dtend = None

        super().save(*args, **kwargs)

    def get_notification_content(self):
        """
        Override this method in subclasses to return the content to be used in the notification.
        Example:
            return f"Event {self.title} is starting soon!"
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_notification(self):
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.id
        notification = Notification.objects.filter(content_type=content_type, object_id=object_id)
        if notification.exists():
            return notification.first()

    def get_next_notification_date(self):
        now = timezone.now()
        if self.is_recurrence:
            return self.recurrence.after(now)

        return self.start_date if self.start_date > now else None

    def get_dates_in_range(self, start_date, end_date):
        if self.is_recurrence:
            return self.recurrence.between(start_date, end_date)

        return [self.start_date] if self.start_date >= start_date and self.start_date <= end_date else []

    def get_notification_update_data(self, data, notification=None):
        """
        Get the data to update the notification object if it exists.
        If the notification object does not exist, it will check if the notification should be created and
        return the data to create it.
        """
        update_data = {}
        notification = notification or self.get_notification()

        try:
            user = self.user
        except AttributeError:
            user = None

        is_user_notifications_active = not user or user.is_notifications_active

        next_notification_date = self.get_next_notification_date()

        if notification and notification.trigger_date != next_notification_date and next_notification_date:
            update_data['trigger_date'] = next_notification_date

        current_is_notifications_active = self.is_notifications_active
        new_is_notifications_active = data.get('is_notifications_active')
        if new_is_notifications_active is not None and new_is_notifications_active != current_is_notifications_active:
            if notification:
                update_data['is_active'] = new_is_notifications_active
            else:
                if new_is_notifications_active and next_notification_date and is_user_notifications_active:
                    update_data = {"user": user, "content_object": self, "trigger_date": next_notification_date}

        return update_data, notification

    def update_object_notification(self, data, notification: Notification = None):
        notification_service = NotificationService()
        update_data, notification = self.get_notification_update_data(data, notification)
        if update_data and notification:
            notification_service.update_notification(notification, update_data)
        elif update_data:
            notification_service.create_notification(update_data)
