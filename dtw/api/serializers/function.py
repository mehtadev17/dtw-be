from rest_framework import serializers
from api.models.function import Function

class FunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Function
        fields = '__all__'
