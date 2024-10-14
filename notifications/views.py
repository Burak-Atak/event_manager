from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, mixins

from core.views import MultiSerializerViewSetMixin
from notifications.filters import NotificationFilter, NotificationLogFilter
from notifications.serializers import *


class NotificationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ("trigger_date",)
    filterset_class = NotificationFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class NotificationLogViewSet(MultiSerializerViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAdminUser]
    serializer_action_classes = {
        'detailed': NotificationLogDetailedSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ("created_date", "notification_type", "status")
    filterset_class = NotificationLogFilter
