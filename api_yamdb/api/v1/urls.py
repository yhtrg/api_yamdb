from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet,
                    UserViewSet, token, signup)

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='User')
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

authpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
    path('token/refresh/', TokenRefreshView.as_view, name='token_refresh')
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(authpatterns))
]
