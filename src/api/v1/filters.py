from django.db.models import F
from django_filters import rest_framework as filters
from django.utils import timezone
import datetime
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
    is_popular = filters.BooleanFilter(
        label='Popular',
        method='filter_by_popularity',
    )
    is_trending = filters.BooleanFilter(
        label='Trending',
        method='filter_by_trending',
    )
    is_featured = filters.BooleanFilter(
        label='Featured',
        method='filter_by_featured',
    )
    new_release = filters.BooleanFilter(
        label='New Release',
        method='filter_new_release',
    )
    top_searched = filters.BooleanFilter(
        label='Top Searched',
        method='filter_by_top_searched',
    )

    class Meta:
        model = DramaSeries
        fields = ['category', 'tag', 'is_popular', 'is_trending', 'is_featured', 'new_release', 'top_searched']

    @staticmethod
    def filter_by_popularity(queryset, name, value):
        """
        Filter based on popularity. Checks if `view_count` exceeds a defined threshold.
        """
        if value:
            return queryset.filter(view_count__gte=1000)  # Threshold can be defined as a constant
        return queryset

    @staticmethod
    def filter_new_release(queryset, name, value):
        """
        Filter for series released in the last 30 days.
        """
        if value:
            thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
            return queryset.filter(release_date__gte=thirty_days_ago)
        return queryset

    @staticmethod
    def filter_by_top_searched(queryset, name, value):
        """
        Filter based on search counts. Assumes a `search_count` field tracks the number of searches.
        """
        if value:
            return queryset.filter(search_count__gte=500)  # Example threshold for top searches
        return queryset

    @staticmethod
    def filter_by_trending(queryset, name, value):
        """
        Filter for trending series based on view count compared to the trending threshold.
        """
        if value:
            return queryset.filter(view_count__gte=F('trending_threshold'))
        return queryset

    @staticmethod
    def filter_by_featured(queryset, name, value):
        """
        Filter for currently featured drama series based on `is_featured` and `featured_until` date.
        """
        if value:
            return queryset.filter(is_featured=True, featured_until__gte=timezone.now().date())
        return queryset
