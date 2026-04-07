from django.contrib import admin
from .models import ProcedureRecordModel
from django.core.exceptions import PermissionDenied


@admin.register(ProcedureRecordModel)
class ProcedureRecordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'procedure__name', 'cbo', 'cnes', 'apac_data__apac_request__establishment__name', 'apac_data__patient_name', 'apac_data']
    search_fields = ['apac_data__pk']
    
    def has_module_permission(self, request):
        """Controla se o app aparece no menu lateral."""
        # Somente usuários staff ou superusuários veem o módulo no menu
        return request.user.is_superuser
    
    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(apac_data__apac_request__establishment__city=request.user.city)

        return qs
    
    def get_readonly_fields(self, request, obj=None):
        editable_fields = [
            'apac_data', 'procedure'
        ]

        if request.user.is_superuser:
            return []

        base_fields = [
            field.name for field in self.model._meta.fields
            if field.name in editable_fields
        ]

        return base_fields