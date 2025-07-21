from django.urls import path
from .views import EstablishmentApiView

urlpatterns = [
    path('apac/', EstablishmentApiView.as_view(), name='apac'),
]