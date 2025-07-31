from django.contrib import admin
from .models import EstablishmentModel


@admin.register(EstablishmentModel)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'city__name', 'cnes', 'cnpj', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['cnes', 'name', 'city__name']