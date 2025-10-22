from django.db import models
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.cid import Cid


class ProcedureModel(models.Model):
    code = models.CharField(verbose_name="Código do Procedimento", max_length=20, db_column='cod_sig_tap')
    name = models.CharField(verbose_name="Nome do Procedimento", max_length=255)
    description = models.CharField(verbose_name="Descrição do Procedimento", max_length=255, null=True, blank=True)
    parents = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="children_recovery",
        blank=True
    )
    mandatory = models.BooleanField(verbose_name="Obrigatório", default=False)
    is_active = models.BooleanField(verbose_name="Está ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'procedimentos'
        verbose_name = "Procedimento"
        verbose_name_plural = "Procedimentos"
    
    def to_entity(self, **kwargs):
        exclude = kwargs.get("exclude_sub_procedures_for_main", None)
        sub_procedures = []
        if not exclude:
            sub_procedures = [children.to_entity(**kwargs) for children in ProcedureModel.objects.filter(parents=self)]

        return Procedure (
            name=self.name,
            code=self.code,
            description=self.description,
            is_active=self.is_active,
            sub_procedures=sub_procedures,
            created_at=self.created_at,
            updated_at=self.updated_at,
            id=self.pk
        )

    def __str__(self):
        return self.name

class CidModel(models.Model):
    code = models.CharField(verbose_name="Código CID", max_length=20, db_column='cod_sig_tap')
    name = models.CharField(verbose_name="Nome CID", max_length=255)
    procedure = models.ForeignKey(
        verbose_name="Procedimento",
        to=ProcedureModel,
        on_delete=models.CASCADE,
        related_name='cid'
    )
    is_active = models.BooleanField(verbose_name="Está ativo", default=True)

    def to_entity(self, **kwargs):
        exclude = kwargs.get("exclude_cid_procedures", None)
 
        return Cid(
            code=self.code,
            name=self.name,
            procedure=None if exclude else self.procedure.to_entity(),
            id=self.pk
        )

    class Meta:
        db_table = 'cid'
        verbose_name = "Cid"
        verbose_name_plural = "Cids"

    def __str__(self):
        return f"{self.code} - {self.name}"