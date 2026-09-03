from django.contrib import admin
from .models import ProcedureModel, CidModel, ProcedureSecondary


class ParentFilter(admin.SimpleListFilter):
    title = 'Parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        # Procedimentos principais = sem pais
        roots = ProcedureModel.objects.filter(parent_links__isnull=True)
        return [("none", "Procedimentos Principais")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(parent_links__isnull=True)
        elif value:
            # filtra procedimentos que possuem esse procedimento como pai
            return queryset.filter(parent_links__parent_id=value)
        return queryset


class CidFilter(admin.SimpleListFilter):
    title = 'Procedure'
    parameter_name = 'procedure'

    def lookups(self, request, model_admin):
        roots = ProcedureModel.objects.filter(parent_links__isnull=True)
        return [("none", "Sem Parent")] + [(obj.pk, str(obj)) for obj in roots]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "none":
            return queryset.filter(procedure__parent_links__isnull=True)
        elif value:
            return queryset.filter(procedure_id=value)
        return queryset


class ProcedureSecondaryInline(admin.TabularInline):
    """Secundários do procedimento (T-037): obrigatório e quantidade máxima são
    do PAR, não do procedimento — por isso vivem aqui, não num campo direto."""
    model = ProcedureSecondary
    fk_name = "parent"
    extra = 0
    autocomplete_fields = ["child"]
    verbose_name = "Procedimento secundário"
    verbose_name_plural = "Procedimentos secundários"


@admin.register(ProcedureModel)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'get_parents', 'fixed_validity_two_competences', 'requires_secondary_cid', 'is_active']
    list_filter = [ParentFilter, 'fixed_validity_two_competences', 'requires_secondary_cid']
    list_editable = ['fixed_validity_two_competences', 'requires_secondary_cid']
    search_fields = ['code', 'name']
    inlines = [ProcedureSecondaryInline]

    def get_parents(self, obj):
        return ", ".join(link.parent.name for link in obj.parent_links.select_related("parent"))
    get_parents.short_description = "Pais"


@admin.register(CidModel)
class CidAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = [CidFilter]
    search_fields = ['code', 'name']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ("procedure", "secondary_of_procedure"):
            # só permite escolher procedimentos principais
            kwargs["queryset"] = ProcedureModel.objects.filter(parent_links__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
