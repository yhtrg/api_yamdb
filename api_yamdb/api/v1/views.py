from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from users.models import User

from reviews.models import Review, Title, Category, Genre

from .permissions import AdminOnly, IsAuthorOrAdmin, IsAdminOrReadOnly
from .serializers import (CustomUserSerializer,
                          SignUpSerializer,
                          UserSerializer,
                          TokenSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReadOnlyTitleSerializer)
from .filters import TitleFilter
from api_yamdb.settings import SIGNUP_EMAIL_MESSAGE

class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    queryset = User.objects.all()


class SignUpViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = user.confirmation_code
            email = user.email
            send_mail(
                SIGNUP_EMAIL_MESSAGE['theme'],
                SIGNUP_EMAIL_MESSAGE['message'] + confirmation_code,
                SIGNUP_EMAIL_MESSAGE['sender'],
                [email, ]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class GetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)


class SelfUserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
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
        serializer: ReviewSerializer,
    ) -> None:
        serializer.save(
            author=self.request.user,
            title=self._title,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
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
        serializer: CommentSerializer,
    ) -> None:
        serializer.save(
            author=self.request.user,
            review=self._review,
        )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return ReadOnlyTitleSerializer
        return TitleSerializer
