import django_filters
from users.models import User

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    date_joined = django_filters.DateFromToRangeFilter()
    modified_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_joined', 'modified_date']