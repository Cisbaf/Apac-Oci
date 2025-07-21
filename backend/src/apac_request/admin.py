from django.contrib import admin
from .models import ApacRequestModel
from django.utils.html import format_html
from django.urls import reverse
from apac_data.models import ApacDataModel
from apac_batch.models import ApacBatchModel
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Painel Administrativo"
admin.site.index_title = "Administração"
admin.site.site_title = "Admin"


class ApacDataInline(admin.StackedInline):
    model = ApacDataModel
    verbose_name = "Dados Apac"
    extra = 0
    can_delete = False
    readonly_fields = ['sub_procedures_readonly']

    def sub_procedures_readonly(self, instance):
        if not instance.pk:
            return "Salve os dados primeiro para ver os sub procedimentos."

        records = instance.records.all()
        if not records:
            return "Nenhum procedimento registrado."

        return format_html_join(
            '\n', "<div><b>{}</b>: {}</div>",
            ((record.procedure.name, record.quantity) for record in records)
        )

    sub_procedures_readonly.short_description = "Sub Procedimentos"

    def get_readonly_fields(self, request, obj=None):
        base_fields = [field.name for field in self.model._meta.fields]
        if request.user.role == "admin":
            return [] + ['sub_procedures_readonly']
        # Adiciona o método customizado ao readonly_fields
        return base_fields + ['sub_procedures_readonly']

class ApacBatchInline(admin.StackedInline):  # ou StackedInline
    model = ApacBatchModel
    verbose_name = "Faixa Apac"
    extra = 0
    can_delete = False  # evita remoção no admin, opcional

    def get_readonly_fields(self, request, obj=None):
        # Retorna todos os campos do modelo como somente leitura
        if request.user.role == "admin":
            return []
        return [field.name for field in self.model._meta.fields]

class Finishedilter(admin.SimpleListFilter):
    title = 'Finalizado'
    parameter_name = 'finished'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.exclude(status="pending")
        if self.value() == 'nao':
            return queryset.exclude(status="approved").exclude(status="approved")
        return queryset
    

@admin.register(ApacRequestModel)
class ApacRequestAdmin(admin.ModelAdmin):
    inlines = [ApacBatchInline, ApacDataInline]
    list_display = ['__str__', 'requester_user',  'establishment', 'city', 'request_date', 'status', 'apac_batch', 'apac_data', 'authorizer', 'review_date', 'finished']
    list_filter = ['status', 'establishment__city', 'establishment', Finishedilter, 'request_date', 'review_date', 'updated_at']

    @admin.display(description="Soliciante")
    def requester_user(self, obj):
        url = reverse("admin:customuser_customuser_change", args=[obj.requester.pk])
        return format_html('<a href="{}">{}</a>', url, f"{obj.requester.first_name} {obj.requester.last_name}")

    @admin.display(description="Cidade")
    def city(self, obj):
        return obj.establishment.city.name
    
    @admin.display(description="Finalizado?", boolean=True)
    def finished(self, obj):
        return obj.status != "pending"

    def get_readonly_fields(self, request, obj=None):
        # Retorna todos os campos do modelo como somente leitura
        if request.user.role == "admin":
            return []
        return [field.name for field in self.model._meta.fields if field.name != 'updated_at']
