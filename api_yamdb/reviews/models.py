from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api_yamdb.settings import MODEL_STR_LIMIT
from users.models import User


class Review(models.Model):
    text = models.TextField(verbose_name = 'Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'Автор'
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name = 'Произведение'
    )
    pub_date = models.DateTimeField(
        verbose_name = 'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = 'reviews'
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:MODEL_STR_LIMIT]


class Comment(models.Model):
    text = models.TextField(verbose_name = 'Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name = 'Отзыв'
    )
    pub_date = models.DateTimeField(
        verbose_name = 'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = 'comments'
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:MODEL_STR_LIMIT]
