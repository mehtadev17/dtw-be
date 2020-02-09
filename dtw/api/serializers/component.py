from rest_framework import serializers
from enumchoicefield import EnumChoiceField
from api.models.component import Component, ComponentTypeChoice


class ComponentSerializer(serializers.ModelSerializer):
    type = EnumChoiceField(enum_class=ComponentTypeChoice)

    class Meta:
        model = Component
        fields = '__all__'
