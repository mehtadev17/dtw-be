from django.contrib.postgres.fields import JSONField
from django.db import models

class Function(models.Model):
    """Function model"""
    name = models.SlugField(max_length=128, null=False, blank=False)
    args = JSONField()
    version = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    