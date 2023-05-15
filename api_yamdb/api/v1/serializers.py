from rest_framework import serializers

from reviews.models import Category, Genres, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genres
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field="slug",
                                         queryset=Genres.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field="slug",
                                            queryset=Category.objects.all())
    
    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating",
                  "description", "genre", "category")


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating",
                  "description", "genre", "category")
        read_only_fields = ("name", "year", "rating",
                            "description", "genre", "category")
