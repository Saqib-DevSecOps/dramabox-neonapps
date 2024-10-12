from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.pagination import DramaSeriesPagination
from src.api.v1.serializers import HomeDramaSeriesListSerializer, DramaSeriesSerializer, DramaSeriesDetailSerializer, \
    ReviewSerializer
from src.services.drama.models import DramaSeries, Review


# Create your views here.

class HomeDramaListAPIView(ListAPIView):
    """
    Provides a list of drama series for the home page.
    Returns featured, trending, upcoming, and new dramas.
    """
    serializer_class = HomeDramaSeriesListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Retrieves and organizes the drama series for the home page.
        Filters dramas into featured, trending, upcoming, and new categories.
        """
        all_dramas = DramaSeries.objects.all()

        featured_dramas = [drama for drama in all_dramas if drama.is_currently_featured][:10]
        trending_dramas = [drama for drama in all_dramas if drama.is_trending][:10]
        upcoming_dramas = DramaSeries.objects.filter(release_date__gt=timezone.now().date())[:10]
        new_dramas = DramaSeries.objects.order_by('-created_at')[:10]

        return {
            'featured_dramas': featured_dramas,
            'trending_dramas': trending_dramas,
            'upcoming_dramas': upcoming_dramas,
            'new_dramas': new_dramas,
        }

    def list(self, request, *args, **kwargs):
        """
        Handles the GET request to retrieve the drama series list.
        Serializes the data and returns the response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class DramaSeriesListAPIView(ListAPIView):
    """
    Provides a paginated list of all drama series.
    Supports search functionality for title and description.
    """
    serializer_class = DramaSeriesSerializer
    permission_classes = [AllowAny]
    pagination_class = DramaSeriesPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        Retrieves all drama series and orders them by their ID.
        """
        return DramaSeries.objects.all().order_by('id')


class DramaSeriesDetailAPIView(RetrieveAPIView):
    """
    Provides detailed information about a specific drama series.
    """
    serializer_class = DramaSeriesDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Retrieves all drama series for detail view.
        """
        return DramaSeries.objects.all()


class ReviewListView(ListAPIView):
    """
    API view to list all reviews for a specific drama series.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter reviews by drama series using the ID provided in the URL
        drama_series_id = self.kwargs.get('drama_series_id')
        if drama_series_id:
            return Review.objects.filter(drama_series_id=drama_series_id)
        return Review.objects.none()  # Return an empty queryset if no drama series is provided


class ReviewCreateView(CreateAPIView):
    """
    API view to create a new review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

