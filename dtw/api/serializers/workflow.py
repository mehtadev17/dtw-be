from rest_framework import serializers
from enumchoicefield import EnumChoiceField
from api.models.component import Component
from api.models.workflow import (
    Workflow,
    WorkflowTypeChoice,
    WorkflowStep,
    WorkflowConnection,
    WorkflowStepSchema,
    WorkflowStepSchemaTypeChoice,
    WorkflowJobConf
)
from api.mixins.item_merge_mixin import ItemMergeMixin


class WorkflowConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkflowConnection
        fields = ('graph', )


class WorkflowStepSchemaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=False)
    type = EnumChoiceField(enum_class=WorkflowStepSchemaTypeChoice)

    class Meta:
        model = WorkflowStepSchema
        fields = ('id', 'type', 'name', 'schema')


class WorkflowStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=False)
    schemas = WorkflowStepSchemaSerializer(many=True, required=False)
    component = serializers.SlugRelatedField(slug_field='name', queryset=Component.objects.all())

    class Meta:
        model = WorkflowStep
        fields = ('id', 'name', 'step_number', 'component', 'parameters', 'schemas', 'mappings')


class WorkflowSerializer(serializers.ModelSerializer, ItemMergeMixin):
    connections = WorkflowConnectionSerializer(many=False, required=False)
    steps = WorkflowStepSerializer(many=True, required=False)
    type = EnumChoiceField(enum_class=WorkflowTypeChoice)

    class Meta:
        model = Workflow
        fields = (
            'id',
            'name',
            'type',
            'description',
            'created_at',
            'updated_at',
            'version',
            'connections',
            'steps'
        )

    def create(self, validated_data):
        connections = validated_data.pop("connections", {})
        steps = validated_data.pop("steps", [])
        workflow = Workflow.objects.create(**validated_data)
        WorkflowConnection.objects.create(workflow=workflow, **connections)

        self.merge_set(
            workflow.steps,
            steps,
            redundant_keys=['id']
        )
        return workflow

    def update(self, instance, validated_data):
        connections = validated_data.pop('connections', {})
        steps = validated_data.pop('steps', [])
        self.merge_set(
            instance.steps,
            steps,
            redundant_keys=['id']
        )

        for key in connections:
            setattr(instance.connections, key, connections[key])
        instance.connections.save()

        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()

        return instance


class WorkflowJobConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkflowJobConf
        fields = ('workflow', 'job')
