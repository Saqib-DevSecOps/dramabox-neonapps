from django_filters import rest_framework as filters

from src.services.drama.models import DramaSeries


class DramaSeriesFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='drama_category__category__name',
        label='Category Name',
    )
    tag = filters.CharFilter(
        field_name='drama_tags__tag__name',
        label='Tag Name',
    )

    class Meta:
        model = DramaSeries
        fields = ['category', 'tag']
