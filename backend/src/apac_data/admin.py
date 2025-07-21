from django.contrib import admin
from .models import ApacDataModel
from procedure_record.models import ProcedureRecordModel

class ProcedureRecordInline(admin.StackedInline):
    model = ProcedureRecordModel
    verbose_name = "Sub Procedimentos"
    extra = 0
    can_delete = False  # evita remoção no admin, opcional

    def get_readonly_fields(self, request, obj=None):
        # Retorna todos os campos do modelo como somente leitura
        if request.user.role == "admin":
            return []
        return [field.name for field in self.model._meta.fields]

# @admin.register(ApacDataModel)
class ApacDataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'patient_name', 'patient_cpf', 'main_procedure', 'procedure_date', 'apac_request']
    list_filter = ['apac_request', 'apac_request__establishment__city','apac_request__establishment', 'apac_request__request_date']
    search_fields = ['patient_name', 'patient_cpf', 'apac_request', 'procedure_date']
    inlines = [ProcedureRecordInline]