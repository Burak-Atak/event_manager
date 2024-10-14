import django_filters

from notifications.models import Notification, NotificationLog



class NotificationFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationLogFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='notification__user')

    class Meta:
        model = NotificationLog
        exclude = ('message',)
