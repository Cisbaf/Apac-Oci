from django.urls import path

urlpatterns = [
    path('api', ApacRequestListCreate.as_view(), name='apac_route'),
]