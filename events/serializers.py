from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from events.models import Event, Category
from core.serializers import RecurrenceSerializer


class CategorySerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    recurrence = RecurrenceSerializer(required=False, write_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        if timezone.now() > attrs.get('start_date'):
            raise serializers.ValidationError(_("Start date must be greater than current date."))

        if attrs.get('start_date') > attrs.get('end_date'):
            raise serializers.ValidationError(_("End date must be greater than start date."))

        return attrs


class EventCalendarQuerySerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)


class EventCalendarResponseSerializer(serializers.Serializer):
    event = EventSerializer()
    dates = serializers.ListField(child=serializers.DateTimeField())
