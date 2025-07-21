from django.contrib import admin
from .models import ProcedureRecordModel
from procedure.models import ProcedureModel


# @admin.register(ProcedureRecordModel)
class ProcedureRecordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'procedure__parent__name', 'procedure__name', 'quantity', 'apac_data__apac_request', 'apac_data']
    list_filter = ['apac_data__apac_request', 'apac_data']
    