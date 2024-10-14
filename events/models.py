from django.db import models
from core.models import StarterModel, NotifiableModel



class Event(StarterModel, NotifiableModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='events', blank=True, null=True)

    def get_notification_content(self):
        return f"Event {self.title} is starting soon!"


class Category(StarterModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
