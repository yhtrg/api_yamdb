from django.core.mail import send_mail
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .permissions import AdminOnly
from .serializers import (CustomUserSerializer,
                          SignUpSerializer,
                          UserSerializer,
                          TokenSerializer)
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