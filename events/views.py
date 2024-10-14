from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from core.views import MultiSerializerViewSetMixin, MultiAuthViewSetMixin
from events.filters import EventFilter, CategoryFilter
from events.models import Event, Category
from events.serializers import EventSerializer, CategorySerializer, EventCalendarResponseSerializer, \
    EventCalendarQuerySerializer
from events.service import EventService, CategoryService


class EventViewSet(MultiSerializerViewSetMixin, MultiAuthViewSetMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    service = EventService()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    serializer_action_classes = {
        'calendar': EventCalendarResponseSerializer,
    }

    authenticated_user_actions = ['create', 'update', 'partial_update', 'destroy']
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = EventFilter
    ordering_fields = ("start_date", "end_date", "created_date")

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        event = self.service.create_event(self.request.user, validated_data)
        serializer.instance = event

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if serializer.instance.user != self.request.user:
            raise PermissionDenied()
        self.service.update_event(serializer.instance, validated_data)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied()
        self.service.delete_event(instance)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def calendar(self, request, *args, **kwargs):
        query_serializer = EventCalendarQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        events = self.service.get_events_calendar(**query_serializer.validated_data, user=request.user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    service = CategoryService()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter
    ordering_fields = ("created_date",)
