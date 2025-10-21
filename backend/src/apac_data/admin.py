from django.contrib import admin
from procedure_record.models import ProcedureRecordModel
from .models import ApacDataModel


class ProcedureRecordInline(admin.StackedInline):
    model = ProcedureRecordModel
    verbose_name = "Sub Procedimentos"
    extra = 0
    can_delete = False  # evita remoção no admin, opcional

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return [field.name for field in self.model._meta.fields]

@admin.register(ApacDataModel)
class ApacDataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'patient_name', 'patient_cpf', 'main_procedure', 'procedure_date', 'apac_request']
    list_filter = [
        'apac_request',
        'apac_request__establishment__city',
        'apac_request__establishment',
        'apac_request__request_date'
    ]
    search_fields = ['patient_name', 'patient_cpf', 'apac_request', 'procedure_date']
    inlines = [ProcedureRecordInline]

    def has_module_permission(self, request):
        """Controla se o app aparece no menu lateral."""
        # Somente usuários staff ou superusuários veem o módulo no menu
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Garante que apenas staff/superuser possam ver o conteúdo."""
        return request.user.is_staff or request.user.is_superuser
