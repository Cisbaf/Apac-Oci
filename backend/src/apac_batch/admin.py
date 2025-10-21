from django.contrib import admin
from django.db.models import Q
from datetime import date
from .models import ApacBatchModel


class AvailableFilter(admin.SimpleListFilter):
    """
    Filtro personalizado no Django Admin para mostrar apenas 
    registros disponíveis ou não disponíveis.
    
    'Disponível' significa que:
      - Ainda não foi associado a um pedido (`apac_request__isnull=True`)
      - E não está vencido (`expire_in` é nulo ou maior/igual à data atual)
    """
    title = 'Disponível'
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        """Define as opções exibidas no filtro lateral do admin."""
        return (
            ('sim', 'Sim'),   # Mostra apenas registros disponíveis
            ('nao', 'Não'),   # Mostra apenas registros indisponíveis
        )

    def queryset(self, request, queryset):
        """Aplica o filtro de acordo com a opção escolhida."""
        today = date.today()

        # Filtra os disponíveis
        if self.value() == 'sim':
            return queryset.filter(
                apac_request__isnull=True
            ).filter(
                Q(expire_in__isnull=True) | Q(expire_in__gte=today)
            )

        # Filtra os não disponíveis
        if self.value() == 'nao':
            return queryset.exclude(
                apac_request__isnull=True,
                expire_in__isnull=True
            ).exclude(
                apac_request__isnull=True,
                expire_in__gte=today
            )

        # Retorna todos se nenhum filtro for aplicado
        return queryset


@admin.register(ApacBatchModel)
class ApacBatchAdmin(admin.ModelAdmin):
    """
    Configuração do modelo ApacBatchModel no Django Admin.
    Define colunas, filtros, campos somente leitura e controle de acesso.
    """
    # Colunas exibidas na lista principal do admin
    list_display = [
        'batch_number', 'created_in', 'expire_in', 'city',
        'apac_request', 'assignment', 'export_date', 'available'
    ]

    # Filtros laterais disponíveis no admin
    list_filter = ['city', AvailableFilter, 'created_in', 'expire_in', 'export_date']

    # Campos pesquisáveis (busca superior)
    search_fields = ['batch_number', 'city__name']

    # Campos somente leitura (não editáveis)
    readonly_fields = ('apac_request', 'export_date')

    @admin.display(description="Data de uso da Faixa")
    def assignment(self, obj):
        """
        Exibe a data de uso (request_date) do pedido vinculado,
        ou vazio se o registro ainda não foi usado.
        """
        return getattr(obj.apac_request, 'request_date', '')

    @admin.display(boolean=True, description='Disponível para uso?')
    def available(self, obj):
        """
        Retorna True se o lote está disponível, ou seja:
        - Não possui apac_request vinculado
        - E ainda não expirou
        """
        if obj.expire_in is None:
            return obj.apac_request is None  # disponível se não tem request
        return obj.apac_request is None and date.today() <= obj.expire_in

    def get_readonly_fields(self, request, obj=None):
        """
        Define os campos como somente leitura para usuários comuns.
        Superusuários podem editar todos os campos.
        """
        if request.user.is_superuser:
            return []
        return [field.name for field in self.model._meta.fields]

    def get_queryset(self, request):
        """
        Restringe os registros visíveis para usuários comuns,
        mostrando apenas registros da mesma cidade que o usuário.
        Superusuários veem todos.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(city=request.user.city)
