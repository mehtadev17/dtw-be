from rest_framework import viewsets
from rest_framework import filters
from api.models.workflow import Workflow
from api.serializers.workflow import WorkflowSerializer



class WorkflowViewSet(viewsets.ModelViewSet):
    """
    View Set for workflows view
    """
    queryset = Workflow.objects.prefetch_related('steps').order_by('id')
    serializer_class = WorkflowSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'type')

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True
        return super(WorkflowViewSet, self).get_serializer(*args, **kwargs)
