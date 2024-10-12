from django.urls import path

from src.services.drama.views import (HomeDramaListAPIView, DramaSeriesListAPIView, DramaSeriesDetailAPIView
                                      )
app_name = 'v1'
urlpatterns = [
    path('home/', HomeDramaListAPIView.as_view(), name='home-drama-list'),
    path('drama/', DramaSeriesListAPIView.as_view(), name='drama-list'),
    path('drama/<str:pk>/', DramaSeriesDetailAPIView.as_view(), name='drama-detail'),

]
