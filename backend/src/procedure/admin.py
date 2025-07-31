from django.contrib import admin
from .models import ProcedureModel, CidModel

class ParentFilter(admin.SimpleListFilter):
    title = 'Parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        # Mostra apenas os registros onde parent é None (nível raiz)
        roots = ProcedureModel.objects.filter(parent__isnull=True)
        return [("none", "Procedimentos Principais")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(parent__isnull=True)
        elif value:
            return queryset.filter(parent_id=value)
        return queryset

class CidFilter(admin.SimpleListFilter):
    title = 'Procedure'
    parameter_name = 'procedure'

    def lookups(self, request, model_admin):
        # Mostra apenas os registros onde parent é None (nível raiz)
        roots = ProcedureModel.objects.filter(parent__isnull=True)
        return [("none", "Sem Parent")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(procedure__parent=None)
        elif value:
            return queryset.filter(procedure_id=value)
        return queryset

@admin.register(ProcedureModel)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent', 'mandatory', 'is_active']
    list_filter = [ParentFilter]
    list_editable = ['mandatory']
    search_fields = ['code', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = ProcedureModel.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(CidModel)
class CidAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'procedure', 'is_active']
    list_filter = [CidFilter]
    search_fields = ['code', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "procedure":
            kwargs["queryset"] = ProcedureModel.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)