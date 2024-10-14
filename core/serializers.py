from rest_framework import serializers
from rest_framework.fields import ChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.enums import Day, Month, Frequency
from recurrence import Recurrence, Rule


class EnumField(ChoiceField):
    default_error_messages = {
        'invalid': _("No matching type.")
    }

    def __init__(self, **kwargs):
        self.enum_type = kwargs.pop("enum_type")
        kwargs.pop("choices", None)
        super(EnumField, self).__init__(self.enum_type.choices(), **kwargs)

    def to_internal_value(self, data):
        for choice in self.enum_type:
            if choice.name == data or choice.value == data:
                return choice.value
        self.fail('invalid')

    def to_representation(self, value):
        if not value:
            return None
        return value.value


class CustomDateTimeField(serializers.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = '%Y-%m-%dT%H:%M'
        kwargs['input_formats'] = ['%Y-%m-%dT%H:%M']
        super(CustomDateTimeField, self).__init__(*args, **kwargs)


class RuleSerializer(serializers.Serializer):
    frequency = EnumField(enum_type=Frequency, source='freq')
    interval = serializers.IntegerField(min_value=1, required=False)
    days_of_week = serializers.ListField(child=EnumField(enum_type=Day), required=False, source='byday')
    days_of_month = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=31),
        required=False,
        source='bymonthday'
    )
    months = serializers.ListField(child=EnumField(enum_type=Month), required=False, source='bymonth')
    position_in_set = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=366), required=False,
                                            source='bysetpos')
    occurrence_count = serializers.IntegerField(required=False, source='count')
    until_date = CustomDateTimeField(required=False, source='until')

    def to_internal_value(self, data):
        data = super(RuleSerializer, self).to_internal_value(data)
        rule = Rule(**data)
        return rule


class RecurrenceSerializer(serializers.Serializer):
    start_date = CustomDateTimeField(required=False, source='dtstart')
    recurrence_rules = RuleSerializer(many=True, source='rrules')
    end_date = CustomDateTimeField(required=False, source='dtend')
    exclusion_rules = RuleSerializer(many=True, required=False, source='exrules')
    include_start_datetime = serializers.BooleanField(required=False, source='include_dtstart')
    recurrence_dates = serializers.ListField(child=CustomDateTimeField(), required=False, source='rdates', )
    exclusion_dates = serializers.ListField(child=CustomDateTimeField(), required=False, source='exdates', )

    def to_internal_value(self, data):
        data = super(RecurrenceSerializer, self).to_internal_value(data)
        recurrence = Recurrence(**data)
        return recurrence

    def validate(self, recurrence: Recurrence):
        if recurrence.dtend and recurrence.dtend < recurrence.dtstart:
            raise serializers.ValidationError(_("End date must be greater than start date."))

        if recurrence.dtstart < timezone.now():
            raise serializers.ValidationError(_("Start date must be greater than current date."))

        return recurrence
