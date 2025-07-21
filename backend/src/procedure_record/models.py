from django.db import models
from procedure.models import ProcedureModel
from apac_core.domain.entities.procedure_record import ProcedureRecord
from apac_data.models import ApacDataModel

class ProcedureRecordModel(models.Model):
    procedure = models.ForeignKey(
        to=ProcedureModel,
        on_delete=models.CASCADE,
        related_name='procedure'
    )
    quantity = models.IntegerField()
    apac_data = models.ForeignKey(
        to=ApacDataModel,
        on_delete=models.CASCADE,
        related_name="records",
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'prodecimentos_apac_registros'
        verbose_name = "Registro Procedimento"
        verbose_name_plural = "Registros Procedimentos"
        
    def to_entity(self):
        return ProcedureRecord(
            procedure=self.procedure.to_entity(),
            quantity=self.quantity,
            id=self.pk
        )

    def __str__(self):
        return f"{self.procedure.name} - {self.quantity}"
    
