from uuid import uuid4

from django.db import models

from parameters.models import Parameter


class ParamToCategorySettings(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    required = models.BooleanField(default=True)

    class Meta:
        unique_together = [('parameter', 'category')]


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    parameters = models.ManyToManyField(
        Parameter, related_name='categories', through=ParamToCategorySettings
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительская категория',
        related_name='children',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'Category: {self.name}'
