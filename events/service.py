from events.models import Event, Category
from notifications.models import Notification
from notifications.service import NotificationService
from django.db import transaction
from django.utils import timezone


class EventService:
    def __init__(self):
        self.notification_service = NotificationService()

    def create_event(self, user, data):
        with transaction.atomic():
            data["user"] = user
            event = Event.objects.create(**data)
            if event.is_notifications_active and user.is_notifications_active:
                notification_data = {"user": user, "content_object": event, "trigger_date": event.start_date}
                self.notification_service.create_notification(notification_data)
        return event

    def update_event(self, event, data):
        with transaction.atomic():
            for attr, value in data.items():
                setattr(event, attr, value)
            event.save()
            event.update_object_notification(data)

        return event

    def get_events_calendar(self, start_date, end_date, user):
        events = []
        if start_date is None:
            start_date = timezone.now()
        if end_date is None:
            end_date = start_date + timezone.timedelta(days=30)
        user_events = Event.objects.filter(user=user).defer("start_date", "end_date", "user")
        for event in user_events:
            dates = event.get_dates_in_range(start_date, end_date)
            if dates:
                events.append({"event": event, "dates": dates})

        return events

    def delete_event(self, event):
        event.delete()
        notification = event.get_notification()
        if notification:
            notification.delete()
        return event


class CategoryService:
    def create_category(self, data):
        return Category.objects.create(**data)

    def update_category(self, category, data):
        for attr, value in data.items():
            setattr(category, attr, value)
        category.save()
        return category
