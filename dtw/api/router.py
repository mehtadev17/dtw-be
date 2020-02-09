from rest_framework import routers
from api.views.workflow import WorkflowViewSet
from api.views.component import ComponentViewSet
from api.views.schema import SchemaViewSet
from api.views.function import FunctionViewSet

#pylint: disable=invalid-name
router = routers.DefaultRouter()
router.register(r'workflow', WorkflowViewSet)
router.register(r'component', ComponentViewSet)
router.register(r'schema', SchemaViewSet)
router.register(r'function', FunctionViewSet)
