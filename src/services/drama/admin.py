from django.contrib import admin
from .models import (
    Category,
    Tag,
    Language,
    ContentRating,
    Actor,
    Director,
    DramaSeries,
    DramaSeriesTag,
    DramaSeriesLanguage,
    DramaSeriesCast,
    Season,
    Episode,
    Review,
    Like, DramaSeriesCategory,
)

# ---------------------------- Utility Models ---------------------------- #

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')


@admin.register(ContentRating)
class ContentRatingAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'created_at', 'updated_at')
    search_fields = ('code',)


# ---------------------------- Person Models ---------------------------- #

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('name',)


# ---------------------------- Main Content Models ---------------------------- #

@admin.register(DramaSeries)
class DramaSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'rating', 'release_date', 'is_featured', 'view_count', 'created_at')
    list_filter = ( 'director', 'rating', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(DramaSeriesTag)
class DramaSeriesTagAdmin(admin.ModelAdmin):
    list_display = ('drama_series', 'tag', 'created_at')
    list_filter = ('tag',)
    search_fields = ('drama_series__title', 'tag__name')


@admin.register(DramaSeriesCategory)
class DramaSeriesCategoryAdmin(admin.ModelAdmin):
    list_display = ('drama_series', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('drama_series__title', 'category__name')


@admin.register(DramaSeriesLanguage)
class DramaSeriesLanguageAdmin(admin.ModelAdmin):
    list_display = ('drama_series', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('drama_series__title', 'language__name')


@admin.register(DramaSeriesCast)
class DramaSeriesCastAdmin(admin.ModelAdmin):
    list_display = ('drama_series', 'actor', 'created_at')
    list_filter = ('drama_series', 'actor')
    search_fields = ('drama_series__title', 'actor__name')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'release_date', 'created_at')
    list_filter = ('series',)
    search_fields = ('series__title',)


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'season', 'episode_number', 'release_date', 'duration', 'is_free', 'view_count', 'created_at')
    list_filter = ('season', 'is_free')
    search_fields = ('title', 'description')


# ---------------------------- User Interaction Models ---------------------------- #

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'drama_series', 'rating', 'created_at')
    list_filter = ('drama_series', 'rating')
    search_fields = ('user__username', 'drama_series__title')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'series', 'liked_on')
    list_filter = ('liked_on',)
    search_fields = ('user__username', 'episode__title', 'series__title')

