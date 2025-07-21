from django.urls import path
from .views import ProcedureApiView

urlpatterns = [
    path('apac/', ProcedureApiView.as_view(), name='apac_procedure'),
]