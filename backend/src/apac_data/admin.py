from django.contrib import admin
from procedure_record.models import ProcedureRecordModel
from .models import ApacDataModel


class ProcedureRecordInline(admin.StackedInline):
    model = ProcedureRecordModel
    verbose_name = "Sub Procedimentos"
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        """
        Evita N+1 queries carregando relações necessárias em uma única query.
        """
        qs = super().get_queryset(request)

        return qs.select_related(
            "procedure",
        )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return [field.name for field in self.model._meta.fields]


@admin.register(ApacDataModel)
class ApacDataAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'patient_name',
        'patient_cpf',
        'main_procedure',
        'procedure_date',
        'apac_request'
    ]

    list_filter = [
        'apac_request',
        'apac_request__establishment__city',
        'apac_request__establishment',
        'apac_request__request_date'
    ]

    search_fields = [
        'patient_name',
        'patient_cpf',
        'apac_request__id',
        'procedure_date'
    ]

    inlines = [ProcedureRecordInline]

    # ==========================
    # OTIMIZAÇÃO DE QUERIES
    # ==========================

    def get_queryset(self, request):
        """
        Resolve o problema de N+1 queries carregando relações com JOIN.
        """

        qs = super().get_queryset(request)

        qs = qs.select_related(
            "main_procedure",
            "apac_request",
            "apac_request__establishment",
            "apac_request__establishment__city",
        ).prefetch_related(
            "records"
        )

        return qs

    # ==========================
    # PERMISSÕES
    # ==========================

    def has_module_permission(self, request):
        """Controla se o app aparece no menu lateral."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Garante que apenas staff/superuser possam ver o conteúdo."""
        return request.user.is_staff or request.user.is_superuser