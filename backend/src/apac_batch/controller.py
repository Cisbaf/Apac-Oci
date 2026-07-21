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

        # select_for_update() trava a linha da faixa escolhida até o fim da
        # transação (a view de aprovação roda sob @transaction.atomic). Sem
        # isso, duas aprovações simultâneas na mesma cidade/competência liam a
        # MESMA faixa como livre (SELECT sem lock, snapshot REPEATABLE READ),
        # ambas gravavam o vínculo, e a segunda sobrescrevia a primeira — que
        # ficava "aprovada" porém órfã de faixa, invisível ao export.
        # order_by('id') garante ordem determinística de varredura (FIFO da
        # faixa mais antiga, evita deadlock por ordens de lock divergentes).
        # No MySQL (produção) o lock é real; no SQLite dos testes é no-op.
        apac_batch = (
            ApacBatchModel.objects
            .select_for_update()
            .annotate(year_part=Substr('batch_number', 3, 2))  # começa em 1, então 3 = 3º caractere
            .filter(
                apac_request=None,
                city__pk=city_id,
                expire_in__gte=date.today(),
                year_part=year_str
            )
            .order_by('id')
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