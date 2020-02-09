from django.db import models
from django.contrib.postgres.fields import JSONField
from enumchoicefield import ChoiceEnum, EnumChoiceField
from api.models.schema import Schema
from api.models.component import Component


class WorkflowTypeChoice(ChoiceEnum):
    STREAMING = "Streaming"
    BATCH = "Batch"


class Workflow(models.Model):
    """Workflow model"""
    name = models.CharField(max_length=128, null=False, blank=False)
    type = EnumChoiceField(WorkflowTypeChoice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)


class WorkflowConnection(models.Model):
    """WorkflowConnection model"""
    workflow = models.OneToOneField(Workflow, related_name='connections', on_delete=models.CASCADE, primary_key=True)
    graph = JSONField(null=True, blank=True)


class WorkflowStep(models.Model):
    """WorkflowStep model"""
    workflow = models.ForeignKey(Workflow, related_name='steps', on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    step_number = models.PositiveIntegerField()
    parameters = JSONField()
    mappings = JSONField(null=True, blank=True)

    class Meta:
        ordering = ['step_number']


class WorkflowStepSchemaTypeChoice(ChoiceEnum):
    INPUT = "Input"
    OUTPUT = "Output"


class WorkflowStepSchema(models.Model):
    """WorkflowStepSchema model"""
    name = models.CharField(max_length=128)
    type = EnumChoiceField(WorkflowStepSchemaTypeChoice)
    workflow_step = models.ForeignKey(WorkflowStep, related_name='schemas', on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)


class WorkflowJobConf(models.Model):
    """WorkflowJobConf model"""
    workflow = models.PositiveIntegerField(null=False, blank=False)
    job = models.PositiveIntegerField(null=True, blank=False, unique=True)
