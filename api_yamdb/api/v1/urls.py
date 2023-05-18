from django.urls import path, include
from .views import TitleViewSet, GenreViewSet, CategoryViewSet
from rest_framework import routers


router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='Category')
router.register('genres', GenreViewSet, basename='Genre')
router.register('titles', TitleViewSet, basename='Title')


urlpatterns = [
    path('v1/', include(router.urls)),
]
