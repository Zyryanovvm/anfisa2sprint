from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг is_published."""
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)

    class Meta:
        abstract = True
