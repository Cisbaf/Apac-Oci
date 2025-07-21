from django.contrib import admin
from .models import ApacBatchModel
from django.db.models import Q
from datetime import date


class AvaliableFilter(admin.SimpleListFilter):
    title = 'Disponível'
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

@admin.register(ApacBatchModel)
class ApacBatchAdmin(admin.ModelAdmin):
    list_display = [
        'batch_number', 'created_in', 'expire_in', 'city', 'apac_request', 'assignment',
        'export_date', 'available'
    ]
    list_filter = ['city', AvaliableFilter, 'created_in', 'expire_in', 'export_date']
    search_fields = ['batch_number', 'city__name']
    readonly_fields = ('apac_request', 'export_date')


    @admin.display(description="Data de uso da Faixa")
    def assignment(self, obj):
        if obj.apac_request:
            return obj.apac_request.request_date
        return ""

    @admin.display(boolean=True, description='Disponível')
    def available(self, obj):
        return obj.apac_request is None and date.today() <= obj.expire_in
