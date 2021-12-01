from uuid import uuid4

from django.db import models


class Manufacturer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'manufacturers'
