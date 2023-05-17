from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Title, Category, Genre
#from api.permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReadOnlyTitleSerializer)
from .filters import TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return ReadOnlyTitleSerializer
        return TitleSerializer
