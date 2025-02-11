from django.urls import path

from src.api.v1.views import (HomeDramaListAPIView, DramaSeriesListAPIView, DramaSeriesDetailAPIView,
                              ReviewListView, ReviewCreateView, LikeCreateView, CategoryTagHelperAPIView,
                              SeasonEpisodeListAPIView, EpisodeWatchProgressCreateApiView,
                              ContinueWatchingListAPIView,ContinueWatchingDeleteAPIView
                              )

app_name = 'v1'
urlpatterns = [
    path('home/', HomeDramaListAPIView.as_view(), name='home-drama-list'),
    path('drama/', DramaSeriesListAPIView.as_view(), name='drama-list'),
    path('drama/<str:pk>/', DramaSeriesDetailAPIView.as_view(), name='drama-detail'),
    path('season/<str:season_id>/episodes/', SeasonEpisodeListAPIView.as_view(), name='season-episode-list'),

]

urlpatterns += [

    path('continue-watching/', ContinueWatchingListAPIView.as_view(), name='continue-watching'),
    path('continue-watching/<str:episode_id>/', ContinueWatchingDeleteAPIView.as_view(), name='continue-watching-delete'),
    path('episode/watch-progress/', EpisodeWatchProgressCreateApiView.as_view(),
         name='episode-watch-progress-create'),
]

urlpatterns += [
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('drama-series/<str:drama_series_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('review/add/', ReviewCreateView.as_view(), name='review-create'),
]

urlpatterns += [
    path('category-tag/helper/', CategoryTagHelperAPIView.as_view(), name='category-tag-helper'),
]
