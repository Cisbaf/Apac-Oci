from django.db import models
from city.models import CityModel
from apac_core.domain.entities.establishment import Establishment
from customuser.models import CustomUser

class EstablishmentModel(models.Model):
    name = models.CharField(verbose_name="Nome do Estabelecimento", max_length=100, unique=True)
    cnes = models.CharField(verbose_name="Cnes Estabelecimento", max_length=15, unique=True)
    city = models.ForeignKey(
        verbose_name="Cidade",
        to=CityModel,
        on_delete=models.CASCADE,
        related_name='establishments'
    )
    cnpj = models.CharField(verbose_name="CNPJ", max_length=14)
    acronym = models.CharField(verbose_name="Sigla", max_length=255)
    restricted_user = models.ManyToManyField(to=CustomUser, verbose_name="Restringir visualização", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Está Ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estabelecimentos'
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"

    def to_entity(self):
        return Establishment(
            name=self.name,
            cnes=self.cnes,
            city=self.city.to_entity(),
            cnpj=self.cnpj,
            acronym=self.acronym,
            is_active=self.is_active,
            id=self.pk
        )

    def __str__(self):
        return self.name
