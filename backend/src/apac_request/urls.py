from django.urls import path
from .views import ApacRequestListCreate, ApacRequestApprovedAPIView, apac_dashboard, ApacRequestRejectAPIView

urlpatterns = [
    path('api', ApacRequestListCreate.as_view(), name='apac_route'),
    path('approved', ApacRequestApprovedAPIView.as_view(), name='approved'),
    path('reject', ApacRequestRejectAPIView.as_view(), name='reject'),
    path("dashboard/", apac_dashboard, name="apac-dashboard"),
]