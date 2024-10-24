import django_filters
from django.forms import TextInput

from src.services.drama.models import Tag, Actor, Language, Category, Director, ContentRating, DramaSeries
from src.services.users.models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}),
                                           lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {}


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Tag name'}), lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']


class ActorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Actor name'}),
                                     lookup_expr='icontains')

    class Meta:
        model = Actor
        fields = ['name']


class LanguageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Language name'}),
                                     lookup_expr='icontains')

    class Meta:
        model = Language
        fields = {}


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Category name'}),
                                     lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']


class DirectorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Director name'}),
                                     lookup_expr='icontains')

    class Meta:
        model = Director
        fields = {}


class ContentRatingFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Content Rating'}),
                                     lookup_expr='icontains')

    class Meta:
        model = ContentRating
        fields = {}

class DramaSeriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Enter Drama Rating'}),
                                     lookup_expr='icontains')

    class Meta:
        model = DramaSeries
        fields = ['title']
