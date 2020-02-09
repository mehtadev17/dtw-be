import django.contrib.postgres.fields
from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField


class SchemaTypeChoice(ChoiceEnum):
    STRUCTURED = "Structured"
    VECTORS = "Vectors"
    XML = "XML"
    CONDITIONAL = "Conditional"


class SchemaFormatChoice(ChoiceEnum):
    DELIMITED = "Delimited"


class Schema(models.Model):
    """Schema model"""
    external_id = models.PositiveIntegerField(null=False, blank=False)
    type = EnumChoiceField(SchemaTypeChoice)
    name = models.CharField(max_length=128, null=False, blank=False)
    ebcdic = models.BooleanField(default=False)
    format = EnumChoiceField(SchemaFormatChoice)
    fields = django.contrib.postgres.fields.JSONField()
