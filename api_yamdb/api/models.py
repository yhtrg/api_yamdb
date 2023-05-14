from django.db import models
from .validators import validate_year


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255)
    year = models.IntegerField(
        verbose_name="Год релиза",
        validators=validate_year)
    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True)
    

    class Meta:
        verbose_name_plural = "Произведение"
        ordering = ['name']
    
    def __str__(self):
        return self.name
