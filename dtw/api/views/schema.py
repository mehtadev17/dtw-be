from rest_framework import viewsets
from rest_framework import filters

from api.models.schema import Schema
from api.serializers.schema import SchemaSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    """
    View Set for schema view
    """
    queryset = Schema.objects.all().order_by('id')
    serializer_class = SchemaSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
