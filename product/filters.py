import django_filters
from .models import Estate, Category, City

class EstateFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(
            title__in=[
                "Коммерческая недвижимость в аренду",
                "Коммерческая недвижимость на продажу",
                "Гаражи в аренду",
                "Гаражи на продажу",
                "Дома в аренду",
                "Дома на продажу",
                "Квартиры в аренду",
                "Квартиры на продажу",
            ]
        ),
        label="Категория"
    )

    class Meta:
        model = Estate
        fields = ['category', 'city', 'price']

    city = django_filters.ModelChoiceFilter(
        field_name='city',
        queryset=City.objects.all(),
        label='Город'
    )

    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='до')

    class Meta:
        model = Estate
        fields = ['category', 'city', 'price_min', 'price_max']