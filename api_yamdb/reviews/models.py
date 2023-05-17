from django.db import models
from .validators import validate_year


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
    

class Genre(models.Model):
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
    genre = models.ManyToManyField(Genre,
                                   verbose_name="Жанр",
                                   blank=True)
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 related_name="titles",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ['name']
    
    def __str__(self):
        return self.name
