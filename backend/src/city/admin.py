from django.contrib import admin
from .models import CityModel

@admin.register(CityModel)
class CityAdmin(admin.ModelAdmin):
    pass

