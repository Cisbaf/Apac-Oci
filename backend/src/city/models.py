from django.db import models
from apac_core.domain.entities.city import City


class CityModel(models.Model):
    name = models.CharField(verbose_name="Nome da cidade", max_length=100, unique=True)
    ibge_code = models.CharField(verbose_name="Código do IBGE", max_length=255, null=True, blank=True)
    agency_name = models.CharField(verbose_name="Nome Agencia", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cidades'
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

    def to_entity(self):
        return City(
            name=self.name,
            ibge_code=self.ibge_code,
            agency_name=self.agency_name,
            id=self.pk
        )

    def __str__(self):
        return self.name