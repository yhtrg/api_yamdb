from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.core.exceptions import ValidationError


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = (
    (ADMIN, 'Администратор'),
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, "Модератор"),)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=150,
        unique=True,
        help_text='Необходимые. 150 символов или меньше.',
        validators=[username_validator],
        error_messages={
            'unique': 'Это имя уже занято.',
        },
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='электронная почта',
        blank=False,
        unique=True,
        max_length=254,
        error_messages={
            'unique': ('электронная почта уже зарегистрирована.'),
        },
    )
    bio = models.TextField(verbose_name="опишите себя", blank=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        verbose_name="роль",
        max_length=60,
        choices=CHOICES,
        null=False,
        default=USER,
    )

    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if self.username == "me":
            return ValidationError("Username не может быть 'me'.")
        else:
            super().save(*args, **kwargs)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    def get_full_name(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return self.username[:15]

    def __str__(self):
        return f"{self.username} is a {self.role}"

    class Meta:

        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"),
                name="Пользователь не может быть назван me!",
            )
        ]
        