from django.contrib import admin
from .models import EstablishmentModel


@admin.register(EstablishmentModel)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'city', 'cnes', 'cnpj', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['cnes', 'name', 'city__name']
    filter_horizontal = ('restricted_user',)

    def get_form(self, request, obj=None, **kwargs):
        """
        Filtra usuários disponíveis no campo restricted_user para a mesma cidade do estabelecimento.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj and hasattr(obj, 'city') and obj.city:
            field = form.base_fields.get('restricted_user')
            if field:
                field.queryset = field.queryset.filter(city=obj.city)
        return form
    

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

    def get_readonly_fields(self, request, obj=None):
        """
        Impede edição de todos os campos exceto 'restricted_user' para usuários que não são superusuários.
        """
        if request.user.is_superuser:
            return []  # Nenhum campo é readonly para superuser
        # Todos os campos do modelo exceto 'restricted_user' ficam readonly
        remove_fields = ['apacrequestmodel', 'id']
        filter_fields = [f for f in self.model._meta.get_fields() if f.name not in remove_fields]
        all_fields = [f.name for f in filter_fields]
        return [f for f in all_fields if f != 'restricted_user']
