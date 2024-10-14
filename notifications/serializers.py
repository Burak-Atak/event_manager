from rest_framework.serializers import ModelSerializer

from notifications.models import Notification, NotificationLog


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationLogSerializer(ModelSerializer):
    class Meta:
        model = NotificationLog
        exclude = ['message']


class NotificationLogDetailedSerializer(ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = '__all__'
