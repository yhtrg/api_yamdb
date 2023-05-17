from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.v1 import serializers
from api.permissions import IsAuthorOrAdmin
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdmin,
    )
    pagination_class = LimitOffsetPagination

    @cached_property
    def _title(self) -> Title:
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self) -> List[Title]:
        return self._title.reviews.all()

    def perform_create(
        self,
        serializer: serializers.ReviewSerializer,
    ) -> None:
        serializer.save(
            author=self.request.user,
            title=self._title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdmin,
    )
    pagination_class = LimitOffsetPagination

    @cached_property
    def _review(self) -> Review:
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self) -> List[Review]:
        return self._review.comments.all()

    def perform_create(
        self,
        serializer: serializers.CommentSerializer,
    ) -> None:
        serializer.save(
            author=self.request.user,
            review=self._review,
        )
