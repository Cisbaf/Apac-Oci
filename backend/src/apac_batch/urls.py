from django.urls import path
from .views import ApacBatchsAvailable, ExportApacBatch

urlpatterns = [
    path('availables', ApacBatchsAvailable.as_view(), name='batchs_avaliables'),
    path('extract', ExportApacBatch.as_view(), name="extract_batch")
]