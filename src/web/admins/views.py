# all_auth
import json

import boto3
from allauth.socialaccount.models import SocialAccount
from botocore.exceptions import ClientError
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
)

from core import settings
from src.services.drama.models import (
    Tag, Actor, Language, Category, Director, ContentRating, DramaSeries, DramaSeriesTag, DramaSeriesLanguage,
    DramaSeriesCategory, Season, Episode
)
from src.services.users.models import User
from src.web.accounts.decorators import staff_required_decorator
from src.web.admins.filters import UserFilter, TagFilter, ActorFilter, LanguageFilter, CategoryFilter, DirectorFilter, \
    ContentRatingFilter, DramaSeriesFilter
from .forms import DramaSeriesTagForm, DramaSeriesLanguageForm, DramaSeriesCategoryForm, SeasonForm, EpisodeForm


@method_decorator(staff_required_decorator, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context = calculate_statistics(context)
        # initialization(init=False, mid=False, end=False)
        return context


""" USERS """


@method_decorator(staff_required_decorator, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(staff_required_decorator, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})


""" SOCIALS """


class SocialsView(TemplateView):
    template_name = 'admins/social-accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['social_accounts'] = SocialAccount.objects.filter(user=self.request.user)
        return context


@method_decorator(staff_required_decorator, name='dispatch')
def remove_social_account(request, account_id):
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
    account.delete()
    return redirect('admins:social-accounts')  # Update with your actual view name or URL name


""" TAGS ---------------------------------------------------------------"""


@method_decorator(staff_required_decorator, name='dispatch')
class TagListView(ListView):
    model = Tag
    template_name = 'admins/tag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_filter = TagFilter(self.request.GET, queryset=Tag.objects.all().order_by('created_at'))

        paginator = Paginator(tag_filter.qs, 20)
        page_number = self.request.GET.get('page')
        tag_page_object = paginator.get_page(page_number)
        context['object_list'] = tag_page_object
        context['tag_filter_form'] = tag_filter.form
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name', 'slug']
    template_name = 'admins/tag_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:tag-list')


@method_decorator(staff_required_decorator, name='dispatch')
class TagCreateView(CreateView):
    model = Tag
    fields = ['name']
    template_name = 'admins/tag_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:tag-list')


@method_decorator(staff_required_decorator, name='dispatch')
class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('admins:tag-list')

    def get(self, request, *args, **kwargs):
        # Directly call the delete method without confirmation
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return HttpResponseRedirect(self.get_success_url())


""" ACTORS -------------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class ActorListView(ListView):
    model = Actor
    template_name = 'admins/actor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor_filter = ActorFilter(self.request.GET, queryset=Actor.objects.all())
        paginator = Paginator(actor_filter.qs, 20)
        page_number = self.request.GET.get('page')
        actor_page_object = paginator.get_page(page_number)
        context['object_list'] = actor_page_object
        context['actor_filter_form'] = actor_filter.form
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class ActorUpdateView(UpdateView):
    model = Actor
    fields = ['name', 'profile_image', 'biography', 'date_of_birth']
    template_name = 'admins/actor_form.html'
    success_url = reverse_lazy('admins:actor-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


@method_decorator(staff_required_decorator, name='dispatch')
class ActorCreateView(CreateView):
    model = Actor
    fields = ['name', 'profile_image', 'biography', 'date_of_birth']
    template_name = 'admins/actor_form.html'
    success_url = reverse_lazy('admins:actor-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


@method_decorator(staff_required_decorator, name='dispatch')
class ActorDeleteView(DeleteView):
    model = Actor
    success_url = reverse_lazy('admins:actor-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


""" Language ---------------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class LanguageListView(ListView):
    model = Language
    template_name = 'admins/language_list.html'  # Update with your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_filter = LanguageFilter(self.request.GET, queryset=Language.objects.all())
        paginator = Paginator(language_filter.qs, 20)  # 50 items per page
        page_number = self.request.GET.get('page')
        language_page_object = paginator.get_page(page_number)
        context['object_list'] = language_page_object
        context['language_filter_form'] = language_filter.form
        return context


# Language Create View
@method_decorator(staff_required_decorator, name='dispatch')
class LanguageCreateView(CreateView):
    model = Language
    fields = ['name', 'code']
    template_name = 'admins/language_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:language-list')


# Language Update View
@method_decorator(staff_required_decorator, name='dispatch')
class LanguageUpdateView(UpdateView):
    model = Language
    fields = ['name', 'code']
    template_name = 'admins/language_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:language-list')


# Language Delete View
@method_decorator(staff_required_decorator, name='dispatch')
class LanguageDeleteView(DeleteView):
    model = Language
    success_url = reverse_lazy('admins:language-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return HttpResponseRedirect(self.get_success_url())


""" CATEGORY ---------------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'admins/category_list.html'  # Update with your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_filter = CategoryFilter(self.request.GET, queryset=Category.objects.all())
        paginator = Paginator(category_filter.qs, 50)
        page_number = self.request.GET.get('page')
        category_page_object = paginator.get_page(page_number)
        context['object_list'] = category_page_object
        context['category_filter_form'] = category_filter.form
        return context


# Category Create View
@method_decorator(staff_required_decorator, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'thumbnail', 'description']
    template_name = 'admins/category_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:category-list')


# Category Update View
@method_decorator(staff_required_decorator, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'slug', 'thumbnail', 'description']
    template_name = 'admins/category_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:category-list')


# Category Delete View
@method_decorator(staff_required_decorator, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('admins:category-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return HttpResponseRedirect(self.get_success_url())


""" DIRECTORS -------------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class DirectorListView(ListView):
    model = Director
    template_name = 'admins/director_list.html'  # Update with your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        director_filter = DirectorFilter(self.request.GET, queryset=Director.objects.all())
        paginator = Paginator(director_filter.qs, 20)  # 50 items per page
        page_number = self.request.GET.get('page')
        director_page_object = paginator.get_page(page_number)
        context['object_list'] = director_page_object
        context['director_filter_form'] = director_filter.form
        return context


# Director Create View
@method_decorator(staff_required_decorator, name='dispatch')
class DirectorCreateView(CreateView):
    model = Director
    fields = ['name', 'profile_image', 'biography', 'date_of_birth']
    template_name = 'admins/director_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:director-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


# Director Update View
@method_decorator(staff_required_decorator, name='dispatch')
class DirectorUpdateView(UpdateView):
    model = Director
    fields = ['name', 'profile_image', 'biography', 'date_of_birth']
    template_name = 'admins/director_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:director-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


# Director Delete View
@method_decorator(staff_required_decorator, name='dispatch')
class DirectorDeleteView(DeleteView):
    model = Director
    success_url = reverse_lazy('admins:director-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return HttpResponseRedirect(self.get_success_url())


""" CONTENT RATING ---------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class ContentRatingListView(ListView):
    model = ContentRating
    template_name = 'admins/contentrating_list.html'  # Update with your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_rating_filter = ContentRatingFilter(self.request.GET, queryset=ContentRating.objects.all())
        paginator = Paginator(content_rating_filter.qs, 1)
        page_number = self.request.GET.get('page')
        contentrating_page_object = paginator.get_page(page_number)
        context['object_list'] = contentrating_page_object
        context['contentrating_filter_form'] = content_rating_filter.form
        return context


@method_decorator(staff_required_decorator, name='dispatch')
class ContentRatingCreateView(CreateView):
    model = ContentRating
    fields = ['code', 'description']
    template_name = 'admins/contentrating_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:content-rating-list')


@method_decorator(staff_required_decorator, name='dispatch')
class ContentRatingUpdateView(UpdateView):
    model = ContentRating
    fields = ['code', 'description']
    template_name = 'admins/contentrating_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:content-rating-list')


@method_decorator(staff_required_decorator, name='dispatch')
class ContentRatingDeleteView(DeleteView):
    model = ContentRating
    success_url = reverse_lazy('admins:content-rating-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object
        return HttpResponseRedirect(self.get_success_url())


""" DRAMA SERIES -------------------------------------------------------- """


class DramaSeriesListView(ListView):
    model = DramaSeries
    template_name = 'admins/dramaseries_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drama_series_filter = DramaSeriesFilter(self.request.GET,
                                                queryset=DramaSeries.objects.all().order_by('-created_at'))
        paginator = Paginator(drama_series_filter.qs, 50)  # 50 items per page
        page_number = self.request.GET.get('page')
        dramaseries_page_object = paginator.get_page(page_number)
        context['object_list'] = dramaseries_page_object
        context['drama_series_filter'] = drama_series_filter.form

        return context


@method_decorator(staff_required_decorator, name='dispatch')
class DramaSeriesCreateView(CreateView):
    model = DramaSeries
    fields = ['poster_image', 'title', 'description',
              'director', 'rating', 'trailer_url',
              'release_date', 'is_featured', 'featured_until'
              ]
    template_name = 'admins/dramaseries_form.html'  # Update with your template path

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['release_date'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['featured_until'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def get_success_url(self):
        return reverse('admins:drama-detail', kwargs={'slug': self.object.slug})


@method_decorator(staff_required_decorator, name='dispatch')
class DramaSeriesUpdateView(UpdateView):
    model = DramaSeries
    fields = ['title', 'description', 'release_date', 'director', 'rating', 'poster_image', 'trailer_url', 'slug',
              'is_featured', 'featured_until', 'trending_threshold']
    template_name = 'admins/dramaseries_form.html'  # Update with your template path
    success_url = reverse_lazy('admins:drama-list')


@method_decorator(staff_required_decorator, name='dispatch')
class DramaSeriesDeleteView(DeleteView):
    model = DramaSeries
    success_url = reverse_lazy('admins:drama-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the object to delete
        self.object.delete()  # Delete the object directly
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(staff_required_decorator, name='dispatch')
class DramaSeriesDetailView(DetailView):
    model = DramaSeries
    template_name = 'admins/dramaseries_detail.html'  # Update with your template path
    context_object_name = 'drama_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add extra context if needed, like related objects
        return context


""" Drama Series Utils ---------------------------------------------------------------------- """


def link_tags_dramaseries(request, slug):
    # Fetch the drama series based on the ID
    drama_series = get_object_or_404(DramaSeries, slug=slug)

    if request.method == 'POST':
        # Process form submission
        form = DramaSeriesTagForm(request.POST)
        if form.is_valid():
            selected_tags = form.cleaned_data['tags']

            # Clear existing tags for this drama series
            DramaSeriesTag.objects.filter(drama_series=drama_series).delete()

            # Link selected tags to the drama series
            for tag in selected_tags:
                DramaSeriesTag.objects.create(drama_series=drama_series, tag=tag)

            # Redirect to a success page or the drama series page
            return redirect('admins:drama-detail', slug=drama_series.slug)
    else:
        # Pre-fill the form with already linked tags
        preselected_tags = Tag.objects.filter(drama_tags__drama_series=drama_series)
        form = DramaSeriesTagForm(initial={'tags': preselected_tags})

    return render(request, 'admins/link_tags_dramaseries.html', {
        'drama_series': drama_series,
        'form': form
    })


def link_languages_dramaseries(request, drama_series_slug):
    # Fetch the drama series based on the slug
    drama_series = get_object_or_404(DramaSeries, slug=drama_series_slug)

    if request.method == 'POST':
        # Process form submission
        form = DramaSeriesLanguageForm(request.POST)
        if form.is_valid():
            selected_languages = form.cleaned_data['languages']

            # Clear existing languages for this drama series
            DramaSeriesLanguage.objects.filter(drama_series=drama_series).delete()

            # Link selected languages to the drama series
            for language in selected_languages:
                DramaSeriesLanguage.objects.create(drama_series=drama_series, language=language)

            # Redirect to a success page or the drama series page
            return redirect('admins:drama-detail', slug=drama_series.slug)
    else:
        # Pre-fill the form with already linked languages
        preselected_languages = Language.objects.filter(drama_languages__drama_series=drama_series)
        form = DramaSeriesLanguageForm(initial={'languages': preselected_languages})

    return render(request, 'admins/link_languages_dramaseries.html', {
        'drama_series': drama_series,
        'form': form
    })


def link_categories_dramaseries(request, drama_series_slug):
    # Fetch the drama series based on the slug
    drama_series = get_object_or_404(DramaSeries, slug=drama_series_slug)

    if request.method == 'POST':
        # Process form submission
        form = DramaSeriesCategoryForm(request.POST)
        if form.is_valid():
            selected_categories = form.cleaned_data['categories']

            # Clear existing categories for this drama series
            DramaSeriesCategory.objects.filter(drama_series=drama_series).delete()

            # Link selected categories to the drama series
            for category in selected_categories:
                DramaSeriesCategory.objects.create(drama_series=drama_series, category=category)

            # Redirect to the drama series detail page
            return redirect('admins:drama-detail', slug=drama_series.slug)
    else:
        # Pre-fill the form with already linked categories
        preselected_categories = DramaSeriesCategory.objects.filter(drama_series=drama_series).values_list('category',
                                                                                                           flat=True)  # Get linked categories
        form = DramaSeriesCategoryForm(initial={'categories': preselected_categories})

    return render(request, 'admins/link_categories_dramaseries.html', {
        'drama_series': drama_series,
        'form': form
    })


""" SEASONS ----------------------------------------------------------------------------------------------  """


@method_decorator(staff_required_decorator, name='dispatch')
class SeasonCreateView(CreateView):
    model = Season
    form_class = SeasonForm
    template_name = 'admins/season_form.html'
    success_url = reverse_lazy('admins:drama-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drama_series_slug = self.kwargs['drama_series_slug']
        context['object'] = get_object_or_404(DramaSeries, slug=drama_series_slug)
        return context

    def form_valid(self, form):
        drama_series_slug = self.kwargs['drama_series_slug']
        drama_series = get_object_or_404(DramaSeries, slug=drama_series_slug)

        # Check if a season with the same number already exists
        season_number = form.cleaned_data['season_number']
        existing_season = Season.objects.filter(series=drama_series, season_number=season_number).first()

        if existing_season:
            form.add_error('season_number', 'A season with this number already exists for this drama series.')
            return self.form_invalid(form)

        form.instance.series = drama_series
        return super().form_valid(form)


class SeasonUpdateView(UpdateView):
    model = Season
    form_class = SeasonForm
    template_name = 'admins/season_form.html'
    context_object_name = 'season'

    def get_success_url(self):
        return reverse_lazy('admins:drama-detail', kwargs={'slug': self.object.series.slug})

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Season, pk=pk)

    def form_valid(self, form):
        return super().form_valid(form)


""" EPISODES ----------------------------------------------------------- """


class SeasonEpisodeListView(DetailView):
    model = Season
    template_name = 'admins/season_episode_list.html'
    context_object_name = 'season'

    def get_object(self, queryset=None):
        drama_series_slug = self.kwargs['drama_series_slug']
        season_pk = self.kwargs['season_pk']
        return get_object_or_404(Season, pk=season_pk, series__slug=drama_series_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes'] = self.object.episodes.order_by('id')
        return context


class SeasonEpisodeCreateView(CreateView):
    template_name = 'admins/season_episode_form.html'
    model = Episode
    form_class = EpisodeForm

    def get_success_url(self):
        season = self.object.season
        # Ensure to get the slug field of the DramaSeries model
        return reverse('admins:season-episode-list',
                       kwargs={'drama_series_slug': season.series.slug, 'season_pk': season.pk})

    def form_valid(self, form):
        season_pk = self.kwargs.get('season_pk')
        form.instance.season = get_object_or_404(Season, pk=season_pk)
        return super().form_valid(form)


class SeasonEpisodeUpdateView(UpdateView):
    template_name = 'admins/season_episode_form.html'
    model = Episode
    form_class = EpisodeForm

    def get_success_url(self):
        season = self.object.season
        return reverse('admins:season-episode-list',
                       kwargs={'drama_series_slug': season.series.slug, 'season_pk': season.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Episode, pk=pk)

    def form_valid(self, form):
        return super().form_valid(form)


class SeasonEpisodeDeleteView(DeleteView):
    model = Episode

    def get_success_url(self):
        season = self.object.season
        return reverse('admins:season-episode-list',
                       kwargs={'drama_series_slug': season.series.slug, 'season_pk': season.pk})

    def delete_s3_objects(self, episode):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        bucket_name = 'dramaboxbucket'
        key_prefix = f"{episode.season.series}/{episode.season}/{episode.video_file_name}"

        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=key_prefix)
        if 'Contents' in response:
            keys_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': keys_to_delete})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.delete_s3_objects(self.object)
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


""" UPLOADS ----------------------------------------------------------- """


@method_decorator(staff_required_decorator, name='dispatch')
class SeasonEpisodeMediaUpdate(TemplateView):
    template_name = 'admins/season_episode_media_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episode'] = get_object_or_404(Episode, pk=self.kwargs.get('pk'))
        return context


@method_decorator(csrf_exempt, name='dispatch')
class SaveFileAPIView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        file_url = data.get('file_url')
        episode_id = data.get('episode_id')
        video_file_name = data.get('file_name')
        episode = get_object_or_404(Episode, pk=episode_id)
        episode.video_file_name = video_file_name
        episode.video_file = file_url
        episode.is_active = True
        episode.save()
        return JsonResponse({'status': 'success', 'message': 'File URL saved successfully.'})
