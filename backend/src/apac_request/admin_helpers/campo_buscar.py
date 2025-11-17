from django.contrib import admin


class CampoBuscaFilter(admin.SimpleListFilter):
    title = 'Campo de busca'
    parameter_name = 'campo_busca'

    def lookups(self, request, model_admin):
        return [
            ('apac_data__patient_name', 'Nome do paciente'),
            ('apac_data__supervising_physician_name', 'Nome do Medico Supervisor'),
            ('apac_data__authorizing_physician_name', 'Nome do Medico Autorizador'),
        ]

    def queryset(self, request, queryset):
        # Não filtramos nada aqui, pois o filtro só serve para escolher o campo
        return queryset
