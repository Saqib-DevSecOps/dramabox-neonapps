from django.urls import path

from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView,
    SocialsView, remove_social_account,
    TagListView, TagDeleteView, TagUpdateView, TagCreateView,
    ActorListView, ActorCreateView, ActorUpdateView, ActorDeleteView,
    LanguageDeleteView, LanguageCreateView, LanguageUpdateView, LanguageListView,
    CategoryUpdateView, CategoryCreateView, CategoryListView, CategoryDeleteView,
    DirectorCreateView, DirectorUpdateView, DirectorDeleteView, DirectorListView,
    ContentRatingListView, ContentRatingCreateView, ContentRatingDeleteView, ContentRatingUpdateView,
    DramaSeriesListView, DramaSeriesDeleteView, DramaSeriesUpdateView, DramaSeriesCreateView, DramaSeriesDetailView,
    link_tags_dramaseries, link_languages_dramaseries, link_categories_dramaseries, SeasonCreateView, SeasonUpdateView,
    SeasonEpisodeListView, SeasonEpisodeCreateView, SeasonEpisodeMediaUpdate, SeasonEpisodeUpdateView, SaveFileAPIView,
    SeasonEpisodeDeleteView
)

app_name = 'admins'
urlpatterns = [

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<str:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<str:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

    path('socials/', SocialsView.as_view(), name='social-accounts'),
    path('remove-social-auth/<str:account_id>/', remove_social_account, name='remove_social_account'),

]

urlpatterns += [

    path('drama-series/', DramaSeriesListView.as_view(), name='drama-list'),
    path('drama-series/create/', DramaSeriesCreateView.as_view(), name='drama-create'),
    path('drama-series/delete/<slug:slug>/', DramaSeriesDeleteView.as_view(), name='drama-delete'),
    path('drama-series/update/<slug:slug>/', DramaSeriesUpdateView.as_view(), name='drama-update'),
    path('drama-series/<slug:slug>/', DramaSeriesDetailView.as_view(), name='drama-detail'),
]

urlpatterns += [
    path('drama-series/<slug:drama_series_slug>/link-languages/', link_languages_dramaseries, name='link-languages'),
    path('drama-series/<slug:slug>/link-tags/', link_tags_dramaseries, name='link-tags-dramaseries'),
    path('drama-series/<slug:drama_series_slug>/link-categories/', link_categories_dramaseries,
         name='link-categories-dramaseries'),

    path('drama-series/<slug:drama_series_slug>/add-season/', SeasonCreateView.as_view(), name='season-create'),
    path('drama-series/<slug:drama_series_slug>/season/<int:pk>/update/', SeasonUpdateView.as_view(),
         name='season-update'),

    path('drama-series/<slug:drama_series_slug>/season/<int:season_pk>/episodes/', SeasonEpisodeListView.as_view(),
         name='season-episode-list'),
    path('drama-series/season/<str:season_pk>/episode/create/', SeasonEpisodeCreateView.as_view(),
         name='episode-create'),
    path('drama-series/season/<str:season_pk>/episode/update/<str:pk>/', SeasonEpisodeUpdateView.as_view(),
         name='episode-update'),

    path('drama-series/season/<str:season_pk>/episode/delete/<str:pk>/', SeasonEpisodeDeleteView.as_view(),
            name='episode-delete'),
    path('drama-series/season/<str:season_pk>/episode/media/update/<str:pk>/', SeasonEpisodeMediaUpdate.as_view(),
         name='episode-media-update'),
]

urlpatterns += [
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('tags/<str:pk>/delete/', TagDeleteView.as_view(), name='tag-delete'),
    path('tags/<str:pk>/update/', TagUpdateView.as_view(), name='tag-update'),

    path('actors/', ActorListView.as_view(), name='actor-list'),
    path('actors/create/', ActorCreateView.as_view(), name='actor-create'),
    path('actors/<str:pk>/update/', ActorUpdateView.as_view(), name='actor-update'),
    path('actors/<str:pk>/delete/', ActorDeleteView.as_view(), name='actor-delete'),

    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('languages/create/', LanguageCreateView.as_view(), name='language-create'),
    path('languages/<str:pk>/update/', LanguageUpdateView.as_view(), name='language-update'),
    path('languages/<str:pk>/delete/', LanguageDeleteView.as_view(), name='language-delete'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<str:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<str:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('directors/', DirectorListView.as_view(), name='director-list'),
    path('directors/create/', DirectorCreateView.as_view(), name='director-create'),
    path('directors/<str:pk>/update/', DirectorUpdateView.as_view(), name='director-update'),
    path('directors/<str:pk>/delete/', DirectorDeleteView.as_view(), name='director-delete'),

    path('content-ratings/', ContentRatingListView.as_view(), name='content-rating-list'),
    path('content-ratings/create/', ContentRatingCreateView.as_view(), name='content-rating-create'),
    path('content-ratings/<str:pk>/update/', ContentRatingUpdateView.as_view(), name='content-rating-update'),
    path('content-ratings/<str:pk>/delete/', ContentRatingDeleteView.as_view(), name='content-rating-delete'),
]


urlpatterns +=[
    path('save-file',SaveFileAPIView.as_view(),name='save-file')
]