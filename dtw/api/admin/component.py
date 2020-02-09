from django.contrib import admin
from api.models.component import Component


class ComponentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Component, ComponentAdmin)
