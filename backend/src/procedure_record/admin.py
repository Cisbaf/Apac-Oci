from django.contrib import admin
from .models import ProcedureRecordModel
from procedure.models import ProcedureModel


@admin.register(ProcedureRecordModel)
class ProcedureRecordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'apac_data']
    list_filter = ['apac_data__apac_request', 'apac_data']
    
    def has_module_permission(self, request):
        """Controla se o app aparece no menu lateral."""
        # Somente usuários staff ou superusuários veem o módulo no menu
        return request.user.is_superuser
