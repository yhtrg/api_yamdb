from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256)
    slug = models.SlugField(
        verbose_name='"slug" категории',
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256)
    slug = models.SlugField(
        verbose_name='"slug" жанра',
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год релиза',
        validators=[validate_year])
    description = models.TextField(
        verbose_name='Описание',
        null=True, blank=True)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   blank=True)
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(settings.MIN_VAL),
                    MaxValueValidator(settings.MAX_VAL)],
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('pub_date',)
        unique_together = [['author', 'title']]

    def __str__(self) -> str:
        return self.text[:settings.MODEL_STR_LIMIT]


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:settings.MODEL_STR_LIMIT]
