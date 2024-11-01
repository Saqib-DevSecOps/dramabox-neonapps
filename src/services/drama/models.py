from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# ---------------------------- Utility Models ---------------------------- #

class Category(models.Model):
    """
    Represents a genre or category of drama, like Drama, Action.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Name of the genre or category.")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier for the category.")
    thumbnail = models.ImageField(upload_to='categories/', blank=True, null=True,
                                  help_text="Thumbnail image for the category.")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the genre or category.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the category was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the category was last updated.")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tags are used for filtering and categorization, such as 'Trending', 'Award-Winning'.
    """
    name = models.CharField(max_length=50, unique=True, help_text="Name of the tag.")
    slug = models.SlugField(max_length=50, unique=True, help_text="URL-friendly identifier for the tag.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the tag was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the tag was last updated.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Represents available languages for drama (e.g., 'English', 'Spanish').
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the language.")
    code = models.CharField(max_length=10, unique=True,
                            help_text="Language code, such as 'en' for English or 'es' for Spanish.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the language was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the language was last updated.")

    def __str__(self):
        return self.name


class ContentRating(models.Model):
    """
    Represents age ratings, such as 'PG', 'R', to enforce drama restrictions.
    """
    code = models.CharField(max_length=10, unique=True, help_text="Content rating code, such as 'PG', 'R'.")
    description = models.CharField(max_length=255, blank=True, null=True,
                                   help_text="Description of the drama rating.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the rating was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the rating was last updated.")

    def __str__(self):
        return self.code


class Person(models.Model):
    """
    Abstract base model for both actors and directors to reuse common fields.
    """
    name = models.CharField(max_length=255, help_text="Full name of the person.")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True,
                                      help_text="Profile image of the person.")
    biography = models.TextField(blank=True, null=True, help_text="Biography of the person.")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Date of birth of the person.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the person was added.")
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text="Date and time when the person's details were last updated.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Actor(Person):
    """
    Represents actors who play roles in various drama series or movies.
    """
    pass


class Director(Person):
    """
    Represents directors of the drama series or movies.
    """
    pass


# ---------------------------- Main Content Models ---------------------------- #

class DramaSeries(models.Model):
    """
    Represents the main series entity containing episodes and seasons.
    """
    title = models.CharField(max_length=255, help_text="Title of the drama series.")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the drama series.")
    release_date = models.DateField(help_text="Release date of the drama series.")
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True,
                                 help_text="Director of the drama series.")
    content_rating = models.ForeignKey(ContentRating, on_delete=models.SET_NULL, null=True,
                                       help_text="Content rating of the drama series.")
    rating = models.DecimalField(max_digits=2, decimal_places=1, help_text="Average rating of the drama series.")
    poster_image = models.ImageField(upload_to='dramas/posters/', blank=True, null=True,
                                     help_text="Poster image of the drama series.")
    trailer_url = models.URLField(blank=True, null=True, help_text="Trailer URL for the drama series.")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier for the drama series.")

    view_count = models.PositiveIntegerField(default=0, help_text="Number of views the drama series has received.")
    search_count = models.PositiveIntegerField(default=0,
                                               help_text="Number of times the drama series has been searched.")

    is_featured = models.BooleanField(default=False, help_text="Mark as featured for promotional purposes.")
    featured_until = models.DateField(blank=True, null=True, help_text="Date until this drama is featured.")

    trending_threshold = models.PositiveIntegerField(default=100, help_text="Minimum views to be considered trending.")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the drama series was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the drama series was last updated.")

    class Meta:
        verbose_name_plural = "Drama Series"

    def __str__(self):
        return self.title

    @property
    def is_currently_featured(self):
        if self.is_featured and self.featured_until:
            return self.featured_until >= timezone.now().date()
        return False

    @property
    def is_trending(self):
        """
        Determines if the drama series is trending based on the view count and the trending threshold.
        Returns True if view_count exceeds the trending_threshold.
        """
        return self.view_count >= self.trending_threshold

    @property
    def upcoming_series(self):
        """
        Returns upcoming series based on release date.
        """
        return self.release_date > timezone.now().date()

    def top_three_series(self):
        """
        Returns top three series based on view count.
        """
        return DramaSeries.objects.order_by('-view_count')[:3]

    @property
    def get_total_episodes(self):
        """
        Returns the total number of episodes.
        """
        return Episode.objects.filter(season__series=self).count()


class DramaSeriesTag(models.Model):
    """
    Normalized Many-to-Many relation for Drama Series and Tags.
    """
    drama_series = models.ForeignKey('DramaSeries', on_delete=models.CASCADE, related_name='drama_tags',
                                     help_text="Linked Drama Series")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='drama_tags', help_text="Linked Tag")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when this tag was added to the series")

    def __str__(self):
        return f"{self.tag.name}"


class DramaSeriesLanguage(models.Model):
    """
    Normalized Many-to-Many relation for Drama Series and Languages.
    """
    drama_series = models.ForeignKey('DramaSeries', on_delete=models.CASCADE, related_name='drama_languages',
                                     help_text="Linked Drama Series")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='drama_languages',
                                 help_text="Linked Language")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when this language was added to the series")

    def __str__(self):
        return f"{self.language.name}"


class DramaSeriesCast(models.Model):
    """
    Normalized Many-to-Many relation for Drama Series and Actors (Cast).
    """
    drama_series = models.ForeignKey('DramaSeries', on_delete=models.CASCADE, related_name='drama_cast',
                                     help_text="Linked Drama Series")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='drama_cast', help_text="Linked Actor")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when this actor was added to the series")

    def __str__(self):
        return f"{self.actor.name}"


class DramaSeriesCategory(models.Model):
    """
    Normalized Many-to-Many relation for Drama Series and Category (Genre).
    """
    drama_series = models.ForeignKey('DramaSeries', on_delete=models.CASCADE, related_name='drama_category',
                                     help_text="Linked Drama Series")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='drama_category',
                                 help_text="Linked Category")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when this actor was added to the series")

    def __str__(self):
        return f"{self.category.name}"

    class Meta:
        verbose_name = "Drama Series Category"
        verbose_name_plural = "Drama Series Categories"


class Season(models.Model):
    """
    Represents a season within a drama series.
    """
    series = models.ForeignKey(DramaSeries, on_delete=models.CASCADE, related_name='seasons',
                               help_text="The drama series this season belongs to.")
    season_number = models.IntegerField(help_text="Season number within the drama series.")
    release_date = models.DateField(help_text="Release date of the season.")
    description = models.TextField(blank=True, null=True, help_text="Description of the season.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the season was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the season was last updated.")

    class Meta:
        unique_together = ('series', 'season_number')
        verbose_name = "Drama Series Season"
        verbose_name_plural = "Drama Series Seasons"

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}"


class Episode(models.Model):
    """
    Represents individual episodes in a specific season of a drama series.
    """
    title = models.CharField(max_length=255, help_text="Title of the episode.")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes',
                               help_text="Season the episode belongs to.")
    episode_number = models.IntegerField(help_text="Episode number within the season.")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the episode.")
    release_date = models.DateField(help_text="Release date of the episode.")
    duration = models.DurationField(help_text="Duration of the episode (hh:mm:ss).")
    video_file_name = models.CharField(max_length=255, blank=True, null=True)
    video_file = models.URLField(null=True, blank=False, help_text="Video file of the episode.")
    is_free = models.BooleanField(default=False, help_text="Mark if the episode is free to watch.")
    view_count = models.PositiveIntegerField(default=0, help_text="Number of views the episode has received.")

    is_active = models.BooleanField(default=False, help_text="Mark if the episode is active.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the episode was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the episode was last updated.")

    class Meta:
        unique_together = ('season', 'episode_number')
        verbose_name = "Drama Series Season Episode"
        verbose_name_plural = "Drama Series Seasons Episode"

    def __str__(self):
        return f"{self.season.series.title} - Season {self.season.season_number}, Episode {self.episode_number}"


# ---------------------------- User Interaction Models ---------------------------- #

class Review(models.Model):
    """
    Represents user reviews for drama series.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, help_text="The user who submitted the review.")
    drama_series = models.ForeignKey(DramaSeries, on_delete=models.CASCADE, related_name='reviews',
                                     help_text="The drama series being reviewed.")
    rating = models.DecimalField(max_digits=2, decimal_places=1, help_text="Rating given by the user (e.g., 4.5).")
    comment = models.TextField(blank=True, null=True, help_text="User's comments about the drama series.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the review was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the review was last updated.")

    class Meta:
        unique_together = ('user', 'drama_series')
        verbose_name = "Drama Series Review"
        verbose_name_plural = "Drama Series Reviews"

    def __str__(self):
        return f"{self.user} - {self.drama_series.title}"


class Like(models.Model):
    """
    Represents likes by users on either an episode or a series.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    drama_series = models.ForeignKey(DramaSeries, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'drama_series')
        verbose_name = "Drama Series Like"
        verbose_name_plural = "Drama Series Likes"

    def __str__(self):
        return f"{self.user.username} liked {self.drama_series.title}"


class Testimonials(models.Model):
    """
    Represents user testimonials for drama series.
    """
    user_name = models.CharField(max_length=255, help_text="Name of the user who submitted the review.")
    user_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, help_text="Rating given by the user (e.g., 4.5).")
    comment = models.TextField(blank=True, null=True, help_text="User's comments about the drama series.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the review was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the review was last updated.")

    class Meta:
        verbose_name = "Drama Series Testimonial"
        verbose_name_plural = "Drama Series Testimonials"
