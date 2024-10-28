import django_filters.widgets
from .models import User
from django.db.models import Q

class UserFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method='filter_term', label='Поиск')
    has_avatar = django_filters.BooleanFilter(method='filter_has_avatar', label='Есть аватар' )
    age_range = django_filters.DateFromToRangeFilter(
        field_name='date_of_birth',
        label='Дата рождения от и до',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )

    def filter_has_avatar(self, queryset, name, value):
        if value:
            return queryset.exclude(avatar='')
        return queryset.filter(avatar='')

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(first_name__icontains=term) | Q(last_name__icontains=term)

        return queryset.filter(criteria).distinct()

    class Meta:
        model = User
        fields = ['term', 'age_range', 'has_avatar']
