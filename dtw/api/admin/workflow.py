from django.contrib import admin
from api.models.workflow import (
    Workflow,
    WorkflowConnection,
    WorkflowStep,
    WorkflowStepSchema,
    WorkflowJobConf
)


class WorkflowAdmin(admin.ModelAdmin):
    pass


class WorkflowConnectionAdmin(admin.ModelAdmin):
    pass


class WorkflowStepAdmin(admin.ModelAdmin):
    pass


class WorkflowStepSchemaAdmin(admin.ModelAdmin):
    pass


class WorkflowJobConfAdmin(admin.ModelAdmin):
    pass


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowConnection, WorkflowConnectionAdmin)
admin.site.register(WorkflowStep, WorkflowStepAdmin)
admin.site.register(WorkflowStepSchema, WorkflowStepSchemaAdmin)
admin.site.register(WorkflowJobConf, WorkflowJobConfAdmin)
