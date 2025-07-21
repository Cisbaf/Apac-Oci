from django.db import models
from customuser.models import CustomUser
from establishment.models import EstablishmentModel
from apac_core.domain.entities.apac_request import ApacRequest
from apac_core.domain.entities.apac_status import ApacStatus

class ApacRequestModel(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        APPROVED = 'approved', 'Aprovada'
        REJECTED = 'rejected', 'Rejeitada'
        
    establishment = models.ForeignKey(
        to=EstablishmentModel,
        on_delete=models.DO_NOTHING,
        verbose_name="Estabelecimento"
    )
    requester = models.ForeignKey(
        to=CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='request',
        verbose_name="Solicitante"
    )
    request_date = models.DateField(
        auto_now_add=True,
        verbose_name="Data da solicitação"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        blank=True,
        null=True,
        verbose_name="Status da solicitação"
    )
    # Autorizador
    authorizer = models.ForeignKey(
        to=CustomUser,
        on_delete=models.DO_NOTHING,
        related_name='authorizer',
        blank=True,
        null=True,
        verbose_name="Autorizador"
    )
    justification = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificativa"
    )
    review_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data da análise"
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de atualização"
    )

    class Meta:
        db_table = 'solicitacoes_apac'
        verbose_name = "Solicitação Apac"
        verbose_name_plural = "Solicitações Apac"

    def to_entity(self):
        try:
            apac_data = self.apac_data
        except:
            apac_data = None
        
        return ApacRequest(
            establishment=self.establishment.to_entity(),
            requester=self.requester.to_entity() if self.requester else None,
            apac_data=apac_data.to_entity() if apac_data else None,
            status=ApacStatus.get(self.status),
            updated_at=self.updated_at,
            request_date=self.request_date,
            authorizer=self.authorizer.to_entity() if self.authorizer else None,
            justification=self.justification,
            review_date=self.review_date,
            id=self.pk
        )

    def __str__(self):
        return f"({self.pk}) {self.establishment.name}"

