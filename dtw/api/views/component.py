from rest_framework import viewsets
from rest_framework import filters
from api.models.component import Component
from api.serializers.component import ComponentSerializer


class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Set for Component
    """
    queryset = Component.objects.all().order_by('id')
    serializer_class = ComponentSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
