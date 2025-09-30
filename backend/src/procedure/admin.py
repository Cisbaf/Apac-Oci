from django.contrib import admin
from .models import ProcedureModel, CidModel


class ParentFilter(admin.SimpleListFilter):
    title = 'Parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        # Procedimentos principais = sem pais
        roots = ProcedureModel.objects.filter(parents__isnull=True)
        return [("none", "Procedimentos Principais")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(parents__isnull=True)
        elif value:
            # filtra procedimentos que possuem esse procedimento como pai
            return queryset.filter(parents__id=value)
        return queryset


class CidFilter(admin.SimpleListFilter):
    title = 'Procedure'
    parameter_name = 'procedure'

    def lookups(self, request, model_admin):
        roots = ProcedureModel.objects.filter(parents__isnull=True)
        return [("none", "Sem Parent")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(procedure__parents=None)
        elif value:
            return queryset.filter(procedure_id=value)
        return queryset


@admin.register(ProcedureModel)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'get_parents', 'mandatory', 'is_active']
    list_filter = [ParentFilter]
    list_editable = ['mandatory']
    search_fields = ['code', 'name']

    def get_parents(self, obj):
        return ", ".join([p.name for p in obj.parents.all()])
    get_parents.short_description = "Pais"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "parents":
            # só permite escolher procedimentos principais como pais
            kwargs["queryset"] = ProcedureModel.objects.filter(parents__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(CidModel)
class CidAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'procedure', 'is_active']
    list_filter = [CidFilter]
    search_fields = ['code', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "procedure":
            kwargs["queryset"] = ProcedureModel.objects.filter(parents__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
