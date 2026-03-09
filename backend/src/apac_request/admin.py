from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from apac_data.models import ApacDataModel
from apac_batch.models import ApacBatchModel
from .models import ApacRequestModel
from establishment.models import EstablishmentModel
from django.utils.formats import date_format
from apac_request.admin_helpers.campo_buscar import CampoBuscaFilter
from apac_request.admin_helpers.competencia_filter import CompetenciaFilter

from django import forms
from django.shortcuts import render
from django.utils import timezone

# Personaliza o cabeçalho e títulos do painel administrativo do Django
admin.site.site_header = "Painel Administrativo"
admin.site.index_title = "Administração"
admin.site.site_title = "Admin"


class StatusForm(forms.Form):
    novo_status = forms.ChoiceField(
        choices=ApacRequestModel.Status.choices,
        label="Novo status"
    )


@admin.action(description="Alterar status...")
def alterar_status(modeladmin, request, queryset):

    if "apply" in request.POST:
        # Aplicar alteração
        novo_status = request.POST["novo_status"]
        ids = request.POST.getlist("selected_ids")

        registros = queryset.filter(pk__in=ids)
        registros.update(
            status=novo_status,
            review_date=timezone.now(),
            authorizer=request.user
        )

        modeladmin.message_user(request, f"{registros.count()} registros atualizados!")
        return

    else:
        # Mostrar página para pedir valor
        form = StatusForm()

        return render(request, "admin/change_status.html", {
            "form": form,
            "queryset": queryset,
            "action": "alterar_status",
        })


# ==========================
# FILTRO PERSONALIZADO: ESTABELECIMENTO
# ==========================

class EstablishmentCityFilter(admin.SimpleListFilter):
    """
    Filtra apenas os estabelecimentos que estão na mesma cidade do usuário.
    Superusuários veem todos.
    """
    title = 'Estabelecimento'
    parameter_name = 'establishment'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            qs = EstablishmentModel.objects.all()
        else:
            qs = EstablishmentModel.objects.filter(city=request.user.city)
        return [(e.id, e.name) for e in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(establishment__id=self.value())
        return queryset


# ==========================
# INLINE: APAC DATA
# ==========================

class ApacDataInline(admin.StackedInline):
    """
    Exibe e gerencia os dados da APAC (ApacDataModel) diretamente
    dentro da tela de edição da requisição (ApacRequestModel).
    """
    model = ApacDataModel
    verbose_name = "Dados Apac"
    extra = 0  # não adiciona formulários extras automaticamente
    can_delete = False  # impede remoção via admin
    readonly_fields = ['sub_procedures_readonly']

    def sub_procedures_readonly(self, instance):
        """
        Exibe uma lista dos subprocedimentos relacionados ao registro atual.
        É apenas leitura, usada como resumo visual dentro do admin.
        """
        if not instance.pk:
            return "Salve os dados primeiro para ver os subprocedimentos."

        records = instance.records.all()
        if not records:
            return "Nenhum procedimento registrado."

        # Renderiza cada subprocedimento em HTML (nome e quantidade)
        header = """
            <table style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr>
                        <th style="text-align:left; padding:4px; border-bottom:1px solid #ccc;">Procedimento</th>
                        <th style="text-align:center; padding:4px; border-bottom:1px solid #ccc;">Qtd</th>
                        <th style="text-align:center; padding:4px; border-bottom:1px solid #ccc;">CBO</th>
                        <th style="text-align:center; padding:4px; border-bottom:1px solid #ccc;">CNES</th>
                    </tr>
                </thead>
                <tbody>
        """

        rows = format_html_join(
            "",
            """
            <tr>
                <td style="padding:4px;">{}</td>
                <td style="text-align:center;">{}</td>
                <td style="text-align:center; color:#555;">{}</td>
                <td style="text-align:center; color:#555;">{}</td>
            </tr>
            """,
            (
                (
                    r.procedure.name,
                    r.quantity,
                    r.cbo or "—",
                    r.cnes or "—",
                )
                for r in records
            ),
        )

        footer = "</tbody></table>"

        return format_html(header) + rows + format_html(footer)


    sub_procedures_readonly.short_description = "Sub Procedimentos"

    def get_readonly_fields(self, request, obj=None):
        """
        Define campos como somente leitura para usuários comuns,
        mas permite edição total para superusuários.
        """
        editable_fields = [
            'cid', 'main_procedure', 'patient_name', 'patient_cns',
            'patient_cpf', 'patient_birth_date',
            'patient_gender'
        ]

        if request.user.is_superuser:
            return []  # superusuário pode editar tudo
        
        # Retorna apenas os campos definidos acima + o campo calculado
        base_fields = [
            field.name for field in self.model._meta.fields
            if field.name in editable_fields
        ]
        return base_fields + ['sub_procedures_readonly']


# ==========================
# INLINE: APAC BATCH
# ==========================

class ApacBatchInline(admin.StackedInline):
    """
    Exibe as informações da Faixa APAC (ApacBatchModel)
    associada à requisição dentro da tela de edição.
    """
    model = ApacBatchModel
    verbose_name = "Faixa Apac"
    extra = 0
    can_delete = False  # impede remoção de faixas no admin

    def get_readonly_fields(self, request, obj=None):
        """
        Usuários comuns não podem editar nenhum campo da faixa.
        Superusuários podem editar tudo.
        """
        if request.user.is_superuser:
            return []
        return [field.name for field in self.model._meta.fields]


# ==========================
# FILTRO PERSONALIZADO
# ==========================

class FinishedFilter(admin.SimpleListFilter):
    """
    Filtro lateral personalizado para exibir apenas registros
    finalizados (status != "pending") ou não finalizados.
    """
    title = 'Processo Finalizado'
    parameter_name = 'finished'

    def lookups(self, request, model_admin):
        """Define as opções que aparecem na lateral do admin."""
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        """Aplica o filtro de acordo com o valor selecionado."""
        if self.value() == 'sim':
            return queryset.exclude(status="pending")  # qualquer status ≠ pending
        if self.value() == 'nao':
            return queryset.filter(status="pending")  # apenas pendentes
        return queryset

# ==========================
# ADMIN: APAC REQUEST
# ==========================

@admin.register(ApacRequestModel)
class ApacRequestAdmin(admin.ModelAdmin):

    inlines = [ApacBatchInline, ApacDataInline]

    list_display = [
        '__str__',
        'competencia_format',
        'requester_user',
        'establishment',
        'paciente_name',
        'procedimento_name',
        'data_preenchimento',
        'review_date',
        'status',
        'finished'
    ]

    search_fields = [
        'apac_batch__batch_number',
        'apac_data__patient_name',
        'apac_data__patient_cpf',
        'apac_data__patient_address_street_name',
        'apac_data__supervising_physician_name',
        'apac_data__authorizing_physician_name',
        'apac_data__main_procedure__name',
        'apac_data__procedure_date',
        'apac_data__discharge_date',
        'request_date',
        'updated_at'
    ]

    list_filter = [
        CompetenciaFilter,
        CampoBuscaFilter,
        'status',
        FinishedFilter,
    ]

    # ==========================
    # OTIMIZAÇÃO PRINCIPAL
    # ==========================

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        qs = qs.select_related(
            "establishment",
            "establishment__city",
            "requester",
            "apac_data",
            "apac_data__main_procedure"
        ).prefetch_related(
            "apac_data__records"
        )

        if not request.user.is_superuser:
            qs = qs.filter(establishment__city=request.user.city)

        return qs

    # ==========================
    # CAMPOS EXIBIDOS
    # ==========================

    @admin.display(description="Procedimento")
    def procedimento_name(self, obj):
        if obj.apac_data and obj.apac_data.main_procedure:
            return obj.apac_data.main_procedure.name
        return "-"

    @admin.display(description="Paciente")
    def paciente_name(self, obj):
        if obj.apac_data:
            return obj.apac_data.patient_name
        return "-"

    @admin.display(description="Data Preenchimento")
    def data_preenchimento(self, obj):
        return obj.updated_at

    @admin.display(description="Competencia")
    def competencia_format(self, obj):
        return date_format(obj.request_date, "F/Y")

    @admin.display(description="Solicitante")
    def requester_user(self, obj):

        if not obj.requester:
            return "-"

        url = reverse(
            "admin:customuser_customuser_change",
            args=[obj.requester.pk]
        )

        full_name = f"{obj.requester.first_name} {obj.requester.last_name}"

        return format_html('<a href="{}">{}</a>', url, full_name)

    @admin.display(description="Cidade")
    def city(self, obj):
        if obj.establishment and obj.establishment.city:
            return obj.establishment.city.name
        return "-"

    @admin.display(description="Autorizado? (Aprovado/Rejeitado)", boolean=True)
    def finished(self, obj):
        return obj.status != "pending"

    # ==========================
    # READONLY FIELDS
    # ==========================

    def get_readonly_fields(self, request, obj=None):

        editable_fields = [
            'request_date',
            'establishment'
        ]

        if request.user.is_superuser:
            return []

        base_fields = [
            field.name
            for field in self.model._meta.fields
            if field.name not in editable_fields
        ]

        return base_fields

    # ==========================
    # BUSCA CUSTOM
    # ==========================

    def get_search_results(self, request, queryset, search_term):

        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term
        )

        campo = request.GET.get('campo_busca')

        if campo and search_term:

            filtro = {
                f"{campo}__icontains": search_term
            }

            queryset = queryset.filter(**filtro)

        return queryset, use_distinct

    # ==========================
    # FILTROS DINÂMICOS
    # ==========================

    def get_list_filter(self, request):

        filters = list(self.list_filter)

        if request.user.is_superuser:
            filters.insert(3, 'establishment__city')
            filters.insert(4, 'establishment')
        else:
            filters.insert(3, EstablishmentCityFilter)

        return filters

    # ==========================
    # LIMITAR ESTABELECIMENTOS
    # ==========================

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "establishment" and not request.user.is_superuser:

            kwargs["queryset"] = EstablishmentModel.objects.filter(
                city=request.user.city
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )