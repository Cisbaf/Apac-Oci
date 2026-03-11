from django.contrib import admin
from django.db.models import Q
from datetime import date
from .models import ApacBatchModel
from city.models import CityModel


class AvailableFilter(admin.SimpleListFilter):
    title = 'Disponível para uso?'
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        today = date.today()

        if self.value() == 'sim':
            return queryset.filter(
                apac_request__isnull=True
            ).filter(
                Q(expire_in__isnull=True) | Q(expire_in__gte=today)
            )

        if self.value() == 'nao':
            return queryset.exclude(
                apac_request__isnull=True,
                expire_in__isnull=True
            ).exclude(
                apac_request__isnull=True,
                expire_in__gte=today
            )

        return queryset


class BatchForCityFilter(admin.SimpleListFilter):
    title = "Cidade"
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            qs = CityModel.objects.all()
            return [(e.id, e.name) for e in qs]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city__id=self.value())
        return queryset


@admin.register(ApacBatchModel)
class ApacBatchAdmin(admin.ModelAdmin):

    list_display = [
        'batch_number',
        'nome_paciente',
        'apac_request',
        'created_in',
        'expire_in',
        'assignment',
        'available'
    ]

    list_filter = [AvailableFilter, BatchForCityFilter]

    search_fields = [
        'created_in',
        'batch_number',
        'apac_request__apac_data__patient_name',
        'apac_request__apac_data__patient_cpf',
        'apac_request__apac_data__patient_address_street_name',
        'apac_request__apac_data__supervising_physician_name',
        'apac_request__apac_data__authorizing_physician_name',
        'apac_request__apac_data__main_procedure__name',
        'apac_request__apac_data__procedure_date',
        'apac_request__apac_data__discharge_date',
        'apac_request__apac_data__supervising_physician_cns',
        'apac_request__apac_data__authorizing_physician_cns'
    ]

    readonly_fields = ('export_date',)

    # ==========================
    # OTIMIZAÇÃO PRINCIPAL
    # ==========================

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        qs = qs.select_related(
            "city",
            "apac_request",
            "apac_request__apac_data",
            "apac_request__apac_data__main_procedure"
        )

        if not request.user.is_superuser:
            qs = qs.filter(city=request.user.city)

        return qs

    # ==========================
    # CAMPOS CALCULADOS
    # ==========================

    @admin.display(description="Paciente")
    def nome_paciente(self, obj):
        if obj.apac_request and obj.apac_request.apac_data:
            return obj.apac_request.apac_data.patient_name
        return ''

    @admin.display(description="Data de uso da Faixa")
    def assignment(self, obj):
        return getattr(obj.apac_request, 'review_date', '')

    @admin.display(boolean=True, description='Disponível para uso?')
    def available(self, obj):

        if obj.expire_in is None:
            return obj.apac_request is None

        return obj.apac_request is None and date.today() <= obj.expire_in

    # ==========================
    # CONTROLE DE EDIÇÃO
    # ==========================

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return []

        return [field.name for field in self.model._meta.fields]