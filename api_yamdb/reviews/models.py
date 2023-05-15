from django.db import models
from api.validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name="Категория",
        max_length=256)
    slug = models.SlugField(
        verbose_name="'slug' категории",
        max_length=50,
        unique=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Genres(models.Model):
    name = models.CharField(
        verbose_name="Жанр",
        max_length=256)
    slug = models.SlugField(
        verbose_name="'slug' жанра",
        max_length=50,
        unique=True)
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=256)
    year = models.IntegerField(
        verbose_name="Год релиза",
        validators=[validate_year])
    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True)
    genre = models.ManyToManyField(Genres,
                                   verbose_name="Жанр",
                                   through="GenreTitle")
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 related_name="titles",
                                 on_delete=models.SET_NULL,
                                 null=True)
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        null=True, default=None)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title,
                              verbose_name="Произведение",
                              on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres,
                              verbose_name="Жанр",
                              on_delete=models.SET_NULL,
                              null=True)
    
    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"
