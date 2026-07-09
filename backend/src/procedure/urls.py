from django.urls import path
from .views import ProcedureApiView, ProcedureAgeAlertApiView

urlpatterns = [
    path('apac/', ProcedureApiView.as_view(), name='apac_procedure'),
    path('apac/check-age-alert', ProcedureAgeAlertApiView.as_view(), name='apac_procedure_age_alert'),
]