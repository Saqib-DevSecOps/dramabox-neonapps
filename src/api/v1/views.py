from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.filters import DramaSeriesFilter
from src.api.v1.pagination import DramaSeriesPagination
from src.api.v1.serializers import HomeDramaSeriesListSerializer, DramaSeriesSerializer, DramaSeriesDetailSerializer, \
    ReviewSerializer, LikeSerializer, CategorySerializer, TagSerializer
from src.services.drama.models import DramaSeries, Review, Like, Episode, Category, Tag


# Create your views here.

class HomeDramaListAPIView(ListAPIView):
    """
    Provides a list of drama series for the home page.
    Returns featured, trending, upcoming, new, seasons for slider, top 10, you might like,
    most popular, new release, and top searched dramas.
    """
    serializer_class = HomeDramaSeriesListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Retrieves and organizes the drama series for the home page.
        Filters dramas into various categories: featured, trending, upcoming, etc.
        """
        all_dramas = DramaSeries.objects.all()
        trending_dramas = [drama for drama in all_dramas if drama.is_trending][:3]
        seasons_for_slider = trending_dramas[:3]
        top_10_dramas = DramaSeries.objects.order_by('-rating')[:10]
        continue_watching = Episode.objects.all()[:10]
        you_might_like = DramaSeries.objects.order_by('?')[:10]
        most_popular = DramaSeries.objects.order_by('-view_count')[:10]
        new_releases = DramaSeries.objects.filter(release_date__gte=timezone.now().date())[:10]
        top_searched = DramaSeries.objects.all()[:10]

        return {
            'trending_slider': seasons_for_slider,
            'continue_watching': continue_watching,
            'top_10_dramas': top_10_dramas,
            'you_might_like': you_might_like,
            'most_popular': most_popular,
            'new_releases': new_releases,
            'top_searched': top_searched,
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = DramaSeriesFilter


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
        drama_series_id = self.kwargs.get('drama_series_id')
        if drama_series_id:
            return Review.objects.filter(drama_series_id=drama_series_id)
        return Review.objects.none()


class ReviewCreateView(CreateAPIView):
    """
    API view to create a new review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeCreateView(CreateAPIView):
    """
    API view to toggle a like for a drama series.
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        drama_series_id = request.data.get('drama_series')
        if not drama_series_id:
            return Response({"detail": "Drama series ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing_like = Like.objects.filter(user=user, drama_series_id=drama_series_id).first()
        if existing_like:
            existing_like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, drama_series_id=drama_series_id)
            return Response({"detail": "Like added."}, status=status.HTTP_201_CREATED)


class CategoryTagHelperAPIView(APIView):
    """
    API view to retrieve all categories or tags.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to retrieve all categories or tags.
        """
        serialize_category = CategorySerializer(Category.objects.all(), many=True)
        serialize_tag = TagSerializer(Tag.objects.all(), many=True)
        return Response({
            'category': serialize_category.data,
            'tag': serialize_tag.data
        })
