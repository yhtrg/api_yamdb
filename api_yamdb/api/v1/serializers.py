from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import EMAIL_LEN, USER_LEN


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator])
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.Serializer):
    queryset = User.objects.all()
    email = serializers.EmailField(max_length=EMAIL_LEN,
                                   allow_blank=False,
                                   required=True,)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      required=True,
                                      max_length=USER_LEN,)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise ValidationError('Имя me недоступно.')

        if User.objects.filter(email=data['email'],
                               username=data['username']).exists():
            return data

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('Этот email уже используется.')

        if User.objects.filter(username=data['username']).exists():
            raise ValidationError('Это имя уже занято.')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = (
            'id',
            'pub_date',
        )

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (author.reviews.filter(title=title_id).exists()
                and method == 'POST'):
            raise serializers.ValidationError('Нельзя оставлять больше одного'
                                              'отзыва!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = (
            'id',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description',
                  'genre', 'category')
