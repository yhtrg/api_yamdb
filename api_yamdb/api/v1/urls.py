from django.urls import path, include
from .views import SelfUserViewSet, SignUpViewSet, UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='User')
router.register('signup', SignUpViewSet, basename='SignUp')
router.register('selfuser', SelfUserViewSet, basename='SelfUser')


urlpatterns = [
    path('v1/', include(router.urls)),
]
