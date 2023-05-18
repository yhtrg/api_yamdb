from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'slug')


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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        read_only_fields = ('name', 'year',
                            'description', 'genre', 'category')
