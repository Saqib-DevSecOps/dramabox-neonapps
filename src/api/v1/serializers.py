from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.services.drama.models import Category, Tag, Language, ContentRating, Actor, Director, DramaSeries, \
    DramaSeriesTag, DramaSeriesLanguage, DramaSeriesCast, DramaSeriesCategory, Season, Episode, Review, Like


# -------------------------GenericSerializer--------------------------------------------

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes data for the Category model.
    Provides fields: id, name, slug, thumbnail, and description.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'thumbnail', 'description']


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Tag model.
    Provides fields: id, name, and slug.
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Language model.
    Provides fields: id, name, and code.
    """

    class Meta:
        model = Language
        fields = ['id', 'name', 'code']


class ContentRatingSerializer(serializers.ModelSerializer):
    """
    Serializes data for the ContentRating model.
    Provides fields: id, code, and description.
    """

    class Meta:
        model = ContentRating
        fields = ['id', 'code', 'description']


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Actor model.
    Provides fields: id, name, profile_image, biography, and date_of_birth.
    """

    class Meta:
        model = Actor
        fields = ['id', 'name', 'profile_image', 'biography', 'date_of_birth']


class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Director model.
    Provides fields: id, name, profile_image, biography, and date_of_birth.
    """

    class Meta:
        model = Director
        fields = ['id', 'name', 'profile_image', 'biography', 'date_of_birth']


class EpisodeHomeSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Episode model.
    Provides essential fields: id, title, episode_number, description, release_date,
    duration, video_file, is_free, view_count, created_at, and updated_at.
    """

    class Meta:
        model = Episode
        fields = ['id', 'title', 'episode_number', 'duration',
                  'video_file', ]


# -------------------------HomeSerializer-----------------------------------------------

class DramaSeriesHomeSerializer(serializers.ModelSerializer):
    """
    Serializes data for the DramaSeries model for the home page.
    Includes related content ratings, categories, tags, and languages.
    """
    categories = serializers.StringRelatedField(many=True, source='drama_category')
    tags = serializers.StringRelatedField(many=True, source='drama_tags')
    languages = serializers.StringRelatedField(many=True, source='drama_languages')

    class Meta:
        model = DramaSeries
        fields = ['id', 'title', 'release_date', 'rating', 'poster_image',
                  'trailer_url', 'slug', 'categories', 'tags', 'languages']


class HomeDramaSeriesListSerializer(serializers.Serializer):
    """
    Aggregates different categories of dramas for the home page response.
    Includes seasons for slider, top 10, you might like, most popular, new releases, and top searched dramas.
    """
    trending_slider = DramaSeriesHomeSerializer(many=True)
    continue_watching = EpisodeHomeSerializer(many=True)
    top_10_dramas = DramaSeriesHomeSerializer(many=True)
    you_might_like = DramaSeriesHomeSerializer(many=True)
    most_popular = DramaSeriesHomeSerializer(many=True)
    new_releases = DramaSeriesHomeSerializer(many=True)
    top_searched = DramaSeriesHomeSerializer(many=True)


# -------------------------DramaSeriesSerializer----------------------------------------

class DramaSeriesSerializer(serializers.ModelSerializer):
    """
    Serializes data for the DramaSeries model.
    Provides fields for general listing of dramas, including nested serializers for related data.
    """
    categories = serializers.StringRelatedField(many=True, source='drama_category')
    tags = serializers.StringRelatedField(many=True, source='drama_tags')
    languages = serializers.StringRelatedField(many=True, source='drama_languages')

    class Meta:
        model = DramaSeries
        fields = ['id', 'title', 'release_date', 'rating', 'poster_image',
                  'trailer_url', 'slug', 'categories', 'tags', 'languages']


class EpisodeSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Episode model.
    Provides essential fields: id, title, episode_number, description, release_date,
    duration, video_file, is_free, view_count, created_at, and updated_at.
    """

    class Meta:
        model = Episode
        fields = ['id', 'title', 'episode_number', 'description', 'release_date', 'duration',
                  'video_file', 'is_free', 'view_count', 'created_at', 'updated_at']


class SeasonSerializer(serializers.ModelSerializer):
    """
    Serializes data for the Season model.
    Includes episodes as nested serializers.
    """
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ['id', 'season_number', 'release_date', 'description', 'episodes', 'created_at', 'updated_at']


class DramaSeriesDetailSerializer(serializers.ModelSerializer):
    """
    Serializes detailed data for the DramaSeries model.
    Includes related director, rating, categories, tags, cast, languages, and seasons.
    """
    director = DirectorSerializer()
    rating = ContentRatingSerializer()
    categories = serializers.StringRelatedField(many=True, source='drama_category')
    tags = serializers.StringRelatedField(many=True, source='drama_tags')
    cast = serializers.StringRelatedField(many=True, source='drama_cast')
    languages = serializers.StringRelatedField(many=True, source='drama_languages')
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = DramaSeries
        fields = ['id', 'title', 'description', 'release_date', 'director', 'rating', 'poster_image',
                  'trailer_url', 'slug', 'view_count', 'categories', 'tags', 'cast', 'languages', 'seasons',
                  'is_trending', 'is_currently_featured', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # Adjust the fields as necessary
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, data):
        """
        Check that the user has not already submitted a review for the specified drama series.
        """
        drama_series = data.get('drama_series')
        user = self.context['request'].user  # Get the authenticated user

        if not drama_series:
            raise ValidationError("Drama series ID is required.")

        if Review.objects.filter(user=user, drama_series=drama_series).exists():
            raise ValidationError("You have already submitted a review for this drama series.")

        return data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['drama_series']  # Make sure to adjust the field name according to your model
        read_only_fields = ['user']
