from rest_framework import viewsets
from rest_framework import filters
from api.models.function import Function
from api.serializers.function import FunctionSerializer

class FunctionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View Set for function view
    """
    queryset = Function.objects.all().order_by('id')
    serializer_class = FunctionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
