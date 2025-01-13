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
    Like, DramaSeriesCategory, Testimonials, EpisodeWatchProgress
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


# ---------------------------- Inline Models ---------------------------- #

# Inline model for DramaSeries Tags
class DramaSeriesTagInline(admin.TabularInline):
    model = DramaSeriesTag
    extra = 1


# Inline model for DramaSeries Category
class DramaSeriesCategoryInline(admin.TabularInline):
    model = DramaSeriesCategory
    extra = 1


# Inline model for DramaSeries Language
class DramaSeriesLanguageInline(admin.TabularInline):
    model = DramaSeriesLanguage
    extra = 1


# Inline model for DramaSeries Cast
class DramaSeriesCastInline(admin.TabularInline):
    model = DramaSeriesCast
    extra = 1


# Inline model for Episode under Season
class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1


# ---------------------------- Main Content Models ---------------------------- #

@admin.register(DramaSeries)
class DramaSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'rating', 'release_date', 'is_featured', 'view_count', 'created_at')
    list_filter = ('director', 'rating', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [DramaSeriesTagInline, DramaSeriesCategoryInline, DramaSeriesLanguageInline, DramaSeriesCastInline]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'release_date', 'created_at')
    list_filter = ('series',)
    search_fields = ('series__title',)
    inlines = [EpisodeInline]  # Add episodes inline under Season


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'season', 'episode_number', 'release_date', 'duration', 'is_free', 'view_count', 'created_at')
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
    list_display = ('user', 'drama_series', 'liked_on')
    list_filter = ('liked_on',)
    search_fields = ('user__username', 'episode__title', 'series__title')


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment', 'created_at')
    search_fields = ('user_name', 'comment', 'message')


@admin.register(EpisodeWatchProgress)
class EpisodeWatchProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'progress', 'timestamp')


admin.site.register(DramaSeriesTag)
