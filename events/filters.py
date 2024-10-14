import django_filters
from events.models import Event, Category


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    category__name = django_filters.CharFilter(lookup_expr='exact', field_name='category__name')

    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date']


class CategoryFilter(django_filters.FilterSet):

    class Meta:
        model = Category
        fields = ['name']
