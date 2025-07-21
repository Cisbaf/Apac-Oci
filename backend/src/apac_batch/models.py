from django.db import models
from city.models import CityModel
from apac_request.models import ApacRequestModel
from apac_core.domain.entities.apac_batch import ApacBatch
from apac_core.domain.value_objects.validity import Validity


class ApacBatchModel(models.Model):
    batch_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Número do lote"
    )
    city = models.ForeignKey(
        to=CityModel,
        on_delete=models.CASCADE,
        verbose_name="Cidade"
    )
    expire_in = models.DateField(
        verbose_name="Data de expiração"
    )
    apac_request = models.OneToOneField(
        to=ApacRequestModel,
        on_delete=models.SET_NULL,
        related_name="apac_batch",
        blank=True,
        null=True,
        verbose_name="Requisição APAC"
    )
    created_in = models.DateField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )
    export_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de exportação"
    )

    class Meta:
        db_table = 'faixas_apac'
        verbose_name = "Lote Apac"
        verbose_name_plural = "Lotes Apac"

    def to_entity(self):
        return ApacBatch(
            batch_number=self.batch_number,
            city=self.city.to_entity(),
            validity=Validity(
                expire_in=self.expire_in,
                created_in=self.created_in
            ),
            apac_request=self.apac_request.to_entity() if self.apac_request else None,
            export_date=self.export_date,
            id=self.pk
        )
    
    def __str__(self):
        return self.batch_number