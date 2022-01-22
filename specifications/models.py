from uuid import uuid4

from django.conf import settings
from django.db import models

from .utils import get_specification_url


class Specification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=settings.DEFAULT_CHAR_FIELD_LENGTH)
    specification_file = models.CharField(
        unique=True, max_length=settings.DEFAULT_CHAR_FIELD_LENGTH
    )
    description = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = 'specifications'

    @property
    def specification_file_url(self) -> str:
        return get_specification_url(self.specification_file)
