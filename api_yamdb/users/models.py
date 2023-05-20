from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, "Модератор"),
    )

    role = models.CharField('Роль', max_length=20,
                            choices=CHOISES, default='user')
    bio = models.TextField(
        verbose_name='О себе',
        null=True, blank=True
    )

    class Meta:
        ordering = ("role",)

    def is_moderator(self):
        return self.role == User.MODERATOR

    def is_admin(self):
        return self.role == User.ADMIN

    def is_user(self):
        return self.role == User.USER
