from django.urls import path

from src.api.v1.views import (HomeDramaListAPIView, DramaSeriesListAPIView, DramaSeriesDetailAPIView,
                              ReviewListView, ReviewCreateView, LikeCreateView
                              )

app_name = 'v1'
urlpatterns = [
    path('home/', HomeDramaListAPIView.as_view(), name='home-drama-list'),
    path('drama/', DramaSeriesListAPIView.as_view(), name='drama-list'),
    path('drama/<str:pk>/', DramaSeriesDetailAPIView.as_view(), name='drama-detail'),

]

urlpatterns += [
    path('drama-series/<str:drama_series_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/add/', ReviewCreateView.as_view(), name='review-create'),
]

urlpatterns +=[
    path('likes/', LikeCreateView.as_view(), name='like-create'),

]