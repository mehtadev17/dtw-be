from rest_framework import serializers
from enumchoicefield import EnumChoiceField
from api.models.schema import Schema, SchemaTypeChoice


class SchemaSerializer(serializers.ModelSerializer):
    type = EnumChoiceField(enum_class=SchemaTypeChoice)

    class Meta:
        model = Schema
        fields = ('id', 'name', 'type', 'ebcdic', 'format', 'fields')

    @staticmethod
    def create(validated_data):
        schema = Schema.objects.create(**validated_data)
        return schema
