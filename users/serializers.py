from rest_framework import serializers

from users.models import User


class NotificationSettingsSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)
    email_allowed = serializers.BooleanField(default=True)
    sms_allowed = serializers.BooleanField(default=True)
    push_allowed = serializers.BooleanField(default=True)


class SettingsSerializer(serializers.Serializer):
    notification_settings = NotificationSettingsSerializer()


class UserDetailedSerializer(serializers.ModelSerializer):
    settings = SettingsSerializer()
    date_joined = serializers.DateTimeField(read_only=True)
    modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'settings', 'first_name', 'last_name',
                  'is_active', 'date_joined', 'phone', 'modified_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'is_active',
                  'date_joined', 'phone', 'modified_date')


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.CharField(required=False)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
