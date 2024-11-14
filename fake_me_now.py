from django.contrib.sites.models import Site
from django.core.validators import validate_email
from django.db import IntegrityError

from faker import Faker

from core.settings import DOMAIN
from src.core.models import Country
from src.services.drama.models import Category, Tag, Language, ContentRating, Director, Actor, DramaSeries, Season, \
    Review, Like, DramaSeriesTag, DramaSeriesLanguage, DramaSeriesCast, DramaSeriesCategory
from src.services.users.models import User

from random import choice, uniform, randint, sample
from django.utils import timezone
import decimal

fake = Faker()

""" HELPERS """


def __print_start(model):
    print()
    print(f"__ BUILD: {model} START __")


def __print_ended(model):
    print(f"__ BUILD: {model} ENDED __")
    print()


""" BASIC """


def basic_configuration():
    sites = Site.objects.all()

    # SITE SETTINGS
    if sites:
        sites = sites[0]
        sites.domain = DOMAIN
        sites.name = DOMAIN
        sites.save()
        print(f"---- Site domain updated to {sites.domain}")
    else:
        Site.objects.create(
            domain=DOMAIN,
            name=DOMAIN,
        )
        print(f"---- Site domain created to {DOMAIN}")


""" GLOBALS """


def country_fake():
    __print_start("Country")
    countries = [
        {
            'name': 'United States',
            'short_name': 'US',
            'language_code': 'en_US',
            'currency_code': 'USD',
            'phone_code': '+1'
        },
        {
            'name': 'United Kingdom',
            'short_name': 'UK',
            'language_code': 'en_GB',
            'currency_code': 'GBP',
            'phone_code': '+44'
        },
        {
            'name': 'Canada',
            'short_name': 'CA',
            'language_code': 'en_CA',
            'currency_code': 'CAD',
            'phone_code': '+1'
        },
    ]

    for country in countries:
        name = country['name']
        short_name = country['short_name']
        language_code = country['language_code']
        currency_code = country['currency_code']
        phone_code = country['phone_code']

        try:
            Country.objects.create(
                name=name, short_name=short_name, language=language_code,
                currency=currency_code,
                phone_code=phone_code
            )

            print(f"---- object: {country['name']} faked.")
        except IntegrityError as e:
            print(e.__str__())

    __print_ended("Country")


""" USER FAKE """


def user_fake():
    __print_start("User")
    users = [
        {
            'username': 'johndoe123',
            'email': 'johndoe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
        },
        {
            'username': 'janedoe456',
            'email': 'janedoe@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'password456',
        },
        {
            'username': 'mikesmith789',
            'email': 'mikesmith@example.com',
            'first_name': 'Mike',
            'last_name': 'Smith',
            'password': 'password789',
        },
        {
            'username': 'sarahconnor',
            'email': 'sarahconnor@example.com',
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'password': 'terminator1',
        },
        {
            'username': 'brucewayne',
            'email': 'brucewayne@example.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'batman123',
        },
    ]

    for user in users:
        email = user['email']
        first_name = user['first_name']
        last_name = user['last_name']
        password = user['password']
        username = user['username']

        try:
            user = User.objects.create_user(email=email, username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.phone_number = fake.phone_number()
            user.bio = fake.text()
            user.address = fake.address()
            user.save()

            print(f"---- object: {email} faked.")
        except IntegrityError as e:
            print(e.__str__())


""" DRAMA FAKE """


def category_fake():
    print("---- Starting to create fake categories ----")

    categories = [
        {
            'name': 'Drama',
            'thumbnail': None,  # Add image paths if desired
            'description': 'Intense, emotional storytelling with complex characters.',
        },
        {
            'name': 'Action',
            'thumbnail': None,
            'description': 'High-energy, fast-paced plots with thrilling scenes.',
        },
        {
            'name': 'Romance',
            'thumbnail': None,
            'description': 'Heartwarming stories focusing on love and relationships.',
        },
        {
            'name': 'Comedy',
            'thumbnail': None,
            'description': 'Light-hearted plots designed to entertain and amuse.',
        },
        {
            'name': 'Mystery',
            'thumbnail': None,
            'description': 'Intriguing plots that keep viewers guessing till the end.',
        },
    ]

    for category_data in categories:
        name = category_data['name']
        thumbnail = category_data['thumbnail']
        description = category_data['description']

        try:
            category = Category.objects.create(
                name=name,
                thumbnail=thumbnail,
                description=description
            )
            print(f"---- Category '{name}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating category '{name}': {e}")

    print("---- Finished creating fake categories ----")


def tag_fake():
    print("---- Starting to create fake tags ----")

    tags = [
        {'name': 'Trending'},
        {'name': 'Award-Winning'},
        {'name': 'New Release'},
        {'name': 'Popular'},
        {'name': 'Classic'}
    ]

    for tag_data in tags:
        name = tag_data['name']

        try:
            tag = Tag.objects.create(name=name)
            print(f"---- Tag '{name}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating tag '{name}': {e}")

    print("---- Finished creating fake tags ----")


def language_fake():
    print("---- Starting to create fake languages ----")

    languages = [
        {'name': 'English', 'code': 'en'},
        {'name': 'Spanish', 'code': 'es'},
        {'name': 'French', 'code': 'fr'},
        {'name': 'German', 'code': 'de'},
        {'name': 'Japanese', 'code': 'ja'}
    ]

    for language_data in languages:
        name = language_data['name']
        code = language_data['code']

        try:
            language = Language.objects.create(name=name, code=code)
            print(f"---- Language '{name}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating language '{name}': {e}")

    print("---- Finished creating fake languages ----")


def content_rating_fake():
    print("---- Starting to create fake content ratings ----")

    ratings = [
        {'code': 'G', 'description': 'General Audience'},
        {'code': 'PG', 'description': 'Parental Guidance'},
        {'code': 'PG-13', 'description': 'Parents Strongly Cautioned'},
        {'code': 'R', 'description': 'Restricted'},
        {'code': 'NC-17', 'description': 'Adults Only'}
    ]

    for rating_data in ratings:
        code = rating_data['code']
        description = rating_data['description']

        try:
            rating = ContentRating.objects.create(code=code, description=description)
            print(f"---- Content rating '{code}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating content rating '{code}': {e}")

    print("---- Finished creating fake content ratings ----")


def person_fake():
    print("---- Starting to create fake actors and directors ----")

    actors = [
        {'name': 'Leonardo DiCaprio'},
        {'name': 'Meryl Streep'},
        {'name': 'Robert Downey Jr.'},
        {'name': 'Scarlett Johansson'},
        {'name': 'Tom Hanks'}
    ]

    directors = [
        {'name': 'Christopher Nolan'},
        {'name': 'Quentin Tarantino'},
        {'name': 'Steven Spielberg'},
        {'name': 'Martin Scorsese'},
        {'name': 'Kathryn Bigelow'}
    ]

    # Create actors
    for actor_data in actors:
        name = actor_data['name']
        biography = fake.text()
        date_of_birth = fake.date_of_birth()

        try:
            actor = Actor.objects.create(
                name=name,
                biography=biography,
                date_of_birth=date_of_birth
            )
            print(f"---- Actor '{name}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating actor '{name}': {e}")

    # Create directors
    for director_data in directors:
        name = director_data['name']
        biography = fake.text()
        date_of_birth = fake.date_of_birth()

        try:
            director = Director.objects.create(
                name=name,
                biography=biography,
                date_of_birth=date_of_birth
            )
            print(f"---- Director '{name}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating director '{name}': {e}")

    print("---- Finished creating fake actors and directors ----")


def drama_series_fake(num_series=10):
    print("---- Starting to create fake drama series ----")

    # Fetch random existing directors and content ratings
    directors = list(Director.objects.all())
    content_ratings = list(ContentRating.objects.all())

    if not directors:
        print("No directors available. Add directors before creating drama series.")
        return

    if not content_ratings:
        print("No content ratings available. Add content ratings before creating drama series.")
        return

    for _ in range(num_series):
        title = fake.sentence(nb_words=3)
        description = fake.paragraph(nb_sentences=5)
        release_date = fake.date_this_decade()
        director = choice(directors)
        content_rating = choice(content_ratings)

        # Generate a random rating between 1.0 and 9.9
        rating = decimal.Decimal(str(round(uniform(1.0, 9.9), 1)))

        trailer_url = fake.url()
        view_count = randint(0, 1000)
        search_count = randint(0, 500)

        is_featured = choice([True, False])
        featured_until = fake.date_between(start_date=timezone.now(), end_date="+30d") if is_featured else None

        trending_threshold = randint(50, 200)

        try:
            drama_series = DramaSeries.objects.create(
                title=title,
                description=description,
                release_date=release_date,
                director=director,
                content_rating=content_rating,
                rating=rating,
                trailer_url=trailer_url,
                view_count=view_count,
                search_count=search_count,
                is_featured=is_featured,
                featured_until=featured_until,
                trending_threshold=trending_threshold
            )
            print(f"---- Drama series '{title}' created successfully.")
        except IntegrityError as e:
            print(f"Error creating drama series '{title}': {e}")

    print("---- Finished creating fake drama series ----")


def drama_series_tag_fake(num_tags_per_series=2):
    """
    Creates fake DramaSeriesTag entries.
    """
    print("---- Creating fake DramaSeriesTag entries ----")
    tags = list(Tag.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    for series in drama_series_list:
        chosen_tags = sample(tags, min(len(tags), num_tags_per_series))  # Choose a subset of tags
        for tag in chosen_tags:
            try:
                DramaSeriesTag.objects.create(drama_series=series, tag=tag)
                print(f"Added tag '{tag.name}' to series '{series.title}'")
            except IntegrityError:
                print(f"Tag '{tag.name}' already exists for series '{series.title}'")


def drama_series_language_fake(num_languages_per_series=2):
    """
    Creates fake DramaSeriesLanguage entries.
    """
    print("---- Creating fake DramaSeriesLanguage entries ----")
    languages = list(Language.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    for series in drama_series_list:
        chosen_languages = sample(languages, min(len(languages), num_languages_per_series))
        for language in chosen_languages:
            try:
                DramaSeriesLanguage.objects.create(drama_series=series, language=language)
                print(f"Added language '{language.name}' to series '{series.title}'")
            except IntegrityError:
                print(f"Language '{language.name}' already exists for series '{series.title}'")


def drama_series_cast_fake(num_actors_per_series=3):
    """
    Creates fake DramaSeriesCast entries.
    """
    print("---- Creating fake DramaSeriesCast entries ----")
    actors = list(Actor.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    for series in drama_series_list:
        chosen_actors = sample(actors, min(len(actors), num_actors_per_series))
        for actor in chosen_actors:
            try:
                DramaSeriesCast.objects.create(drama_series=series, actor=actor)
                print(f"Added actor '{actor.name}' to series '{series.title}'")
            except IntegrityError:
                print(f"Actor '{actor.name}' already exists for series '{series.title}'")


def drama_series_category_fake(num_categories_per_series=2):
    """
    Creates fake DramaSeriesCategory entries.
    """
    print("---- Creating fake DramaSeriesCategory entries ----")
    categories = list(Category.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    for series in drama_series_list:
        chosen_categories = sample(categories, min(len(categories), num_categories_per_series))
        for category in chosen_categories:
            try:
                DramaSeriesCategory.objects.create(drama_series=series, category=category)
                print(f"Added category '{category.name}' to series '{series.title}'")
            except IntegrityError:
                print(f"Category '{category.name}' already exists for series '{series.title}'")




def season_fake(num_seasons_per_series=3):
    print("---- Starting to create fake seasons ----")

    # Get all available drama series
    drama_series_list = list(DramaSeries.objects.all())

    if not drama_series_list:
        print("No drama series available. Add drama series before creating seasons.")
        return

    for series in drama_series_list:
        for season_num in range(1, num_seasons_per_series + 1):
            release_date = fake.date_between(start_date=series.release_date, end_date="+2y")
            description = fake.paragraph(nb_sentences=4)

            try:
                season = Season.objects.create(
                    series=series,
                    season_number=season_num,
                    release_date=release_date,
                    description=description
                )
                print(f"---- Season {season_num} for series '{series.title}' created successfully.")
            except IntegrityError as e:
                print(f"Error creating Season {season_num} for '{series.title}': {e}")

    print("---- Finished creating fake seasons ----")


def review_fake(num_reviews_per_series=5):
    print("---- Starting to create fake reviews ----")

    # Get all available users and drama series
    users = list(User.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    if not users or not drama_series_list:
        print("No users or drama series available. Add users and drama series before creating reviews.")
        return

    for series in drama_series_list:
        for _ in range(num_reviews_per_series):
            user = fake.random_element(users)  # Randomly choose a user for each review
            rating = round(uniform(1, 5), 1)  # Generate a rating between 1.0 and 5.0
            comment = fake.paragraph(nb_sentences=randint(1, 5))  # Generate a comment with 1-5 sentences

            try:
                review = Review.objects.create(
                    user=user,
                    drama_series=series,
                    rating=rating,
                    comment=comment
                )
                print(f"---- Review by {user.username} for '{series.title}' created successfully.")
            except IntegrityError as e:
                print(f"Error creating review for '{series.title}': {e}")

    print("---- Finished creating fake reviews ----")


def like_fake(num_likes_per_series=3):
    print("---- Starting to create fake likes ----")

    # Get all available users and drama series
    users = list(User.objects.all())
    drama_series_list = list(DramaSeries.objects.all())

    if not users or not drama_series_list:
        print("No users or drama series available. Add users and drama series before creating likes.")
        return

    for series in drama_series_list:
        selected_users = set()

        for _ in range(num_likes_per_series):
            user = choice(users)

            # Ensure each user can only like a series once
            if user in selected_users:
                continue

            selected_users.add(user)

            try:
                like = Like.objects.create(
                    user=user,
                    drama_series=series
                )
                print(f"---- {user.username} liked '{series.title}' successfully.")
            except IntegrityError as e:
                print(f"Error creating like for '{series.title}' by {user.username}: {e}")

    print("---- Finished creating fake likes ----")


""" ============================================================================================== """


def main():
    # basic_configuration()
    # country_fake()
    # user_fake()

    # category_fake()
    # tag_fake()
    # language_fake()
    # content_rating_fake()
    # person_fake()

    # drama_series_fake()
    # season_fake()
    # review_fake()
    # like_fake()

    drama_series_tag_fake()
    drama_series_language_fake()
    drama_series_cast_fake()
    drama_series_category_fake()


if __name__ == '__main__':
    main()
