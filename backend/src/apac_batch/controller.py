from .models import ApacBatchModel
from apac_request.models import ApacRequestModel
from datetime import date
from apac_core.domain.repositories.apac_batch_repository import ApacBatchRepository
from apac_core.domain.exceptions import NotFoundException
from apac_core.domain.messages.apac_request_messages import NO_BATCH_AVAILABLE
from django.db.models.functions import Substr

class ApacBatchController(ApacBatchRepository):

    def get_by_id(self, batch_id):
        batch = ApacBatchModel.objects.get(pk=batch_id)
        if batch:
            return batch.to_entity()
        return NotFoundException()

    def search_for_available_batch(self, city_id, competence):
        year_2_digits = competence.year % 100
        year_str = f"{year_2_digits:02d}"      # garante 2 dígitos

        apac_batch = (
            ApacBatchModel.objects
            .annotate(year_part=Substr('batch_number', 3, 2))  # começa em 1, então 3 = 3º caractere
            .filter(
                apac_request=None,
                city__pk=city_id,
                expire_in__gte=date.today(),
                year_part=year_str
            )
        )

        if apac_batch:
            return apac_batch.first().to_entity()
        raise NotFoundException(NO_BATCH_AVAILABLE)
    
    def save(self, apac_batch):
        if apac_batch.id:
            apac_batch_model = ApacBatchModel.objects.get(pk=apac_batch.id)
            apac_batch_model.apac_request = ApacRequestModel.objects.get(pk=apac_batch.apac_request.id)
            apac_batch_model.save()
            return apac_batch_model.to_entity()
        return apac_batch