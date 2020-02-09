from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField


class ComponentTypeChoice(ChoiceEnum):
    Source = "Source"
    Transform = "Transform"
    Sink = "Sink"


class Component(models.Model):
    """Component model"""
    name = models.SlugField(max_length=128, null=False, blank=False)
    type = EnumChoiceField(ComponentTypeChoice)
    description = models.TextField(null=False, blank=False)
