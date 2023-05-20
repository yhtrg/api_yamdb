from django.urls import path, include
from .views import (SelfUserViewSet, SignUpViewSet,
                    UserViewSet, TitleViewSet,
                    GenreViewSet, CategoryViewSet,
                    ReviewViewSet, CommentViewSet)
from rest_framework import routers


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='User')
router.register('signup', SignUpViewSet, basename='SignUp')
router.register('selfuser', SelfUserViewSet, basename='SelfUser')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router.register('categories', CategoryViewSet, basename='Category')
router.register('genres', GenreViewSet, basename='Genre')
router.register('titles', TitleViewSet, basename='Title')


urlpatterns = [
    path('v1/', include(router.urls)),
]
