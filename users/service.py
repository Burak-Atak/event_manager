from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from django.conf import settings
from users.models import User
from users.serializers import SettingsSerializer
from notifications.models import Notification
from notifications.service import NotificationService


class UserService:
    def __init__(self):
        self.notification_service = NotificationService()

    def register_user(self, validated_data, is_admin=False):
        validated_data['settings'] = SettingsSerializer(settings.DEFAULT_USER_SETTINGS).data
        if is_admin:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def login_user(self, validated_data):
        user = authenticate(**validated_data)
        if user is None:
            raise AuthenticationFailed()

        token, _ = Token.objects.get_or_create(user=user)

        return {'token': f"Token {token.key}", 'user': user}

    def update_user(self, user, data):
        with transaction.atomic():
            current_is_user_notification_active = user.settings.get('notification_settings', {}).get('is_active', None)
            for attr, value in data.items():
                setattr(user, attr, value)
            user.save()

            new_is_user_notification_active = user.settings.get('notification_settings', {}).get('is_active', None)

            if current_is_user_notification_active != new_is_user_notification_active:
                user_notifications = Notification.objects.filter(user=user)
                data = {"is_active": new_is_user_notification_active}
                self.notification_service.bulk_update_notifications(user_notifications, data)

        return user
