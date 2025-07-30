from django.db import models
from procedure.models import ProcedureModel, CidModel
from apac_request.models import ApacRequestModel
from apac_core.domain.entities.apac_data import ApacData


class ApacDataModel(models.Model):
    apac_request = models.OneToOneField(
        to=ApacRequestModel,
        on_delete=models.CASCADE,
        related_name="apac_data",
        blank=True,
        null=True,
        verbose_name="Solcitação APAC"
    )
    patient_name = models.CharField(max_length=255, verbose_name="Nome do paciente")
    patient_record_number = models.CharField(max_length=255, verbose_name="Número do prontuário")
    patient_cns = models.CharField(max_length=255, verbose_name="CNS do paciente")
    patient_cpf = models.CharField(max_length=255, verbose_name="CPF do paciente")
    # patient_birth_date = models.CharField(max_length=255, verbose_name="Data de nascimento do paciente")
    patient_birth_date = models.DateField(verbose_name="Data de nascimento do paciente")
    patient_race_color = models.CharField(max_length=255, verbose_name="Raça/cor do paciente")
    patient_gender = models.CharField(max_length=255, verbose_name="Gênero do paciente")
    patient_mother_name = models.CharField(max_length=255, verbose_name="Nome da mãe do paciente")
    patient_address_street_type = models.CharField(max_length=255, verbose_name="Tipo de logradouro")
    patient_address_street_name = models.CharField(max_length=255, verbose_name="Nome do logradouro")
    patient_address_number = models.CharField(max_length=255, verbose_name="Número do endereço")
    patient_address_complement = models.CharField(max_length=255, verbose_name="Complemento do endereço")
    patient_address_postal_code = models.CharField(max_length=255, verbose_name="CEP")
    patient_address_neighborhood = models.CharField(max_length=255, verbose_name="Bairro")
    patient_address_city = models.CharField(max_length=255, verbose_name="Cidade")
    patient_address_state = models.CharField(max_length=255, verbose_name="Estado")
    medic_name = models.CharField(max_length=255, verbose_name="Nome do médico")
    medic_cns = models.CharField(max_length=255, verbose_name="CNS do médico")
    medic_cbo = models.CharField(max_length=255, verbose_name="CBO do médico")
    main_procedure = models.ForeignKey(to=ProcedureModel, on_delete=models.DO_NOTHING, verbose_name="Procedimento principal")
    # procedure_date = models.CharField(max_length=255, verbose_name="Data do procedimento")
    procedure_date = models.DateField(verbose_name="Data do procedimento")
    cid = models.ForeignKey(to=CidModel, on_delete=models.DO_NOTHING, verbose_name="CID")

    class Meta:
        db_table = 'dados_apac'
        verbose_name = "Dado Apac"
        verbose_name_plural = "Dados Apac"

    def __str__(self):
        return f"{self.pk}"

    def to_entity(self):
        try:
            records = self.records.all()
        except:
            records = None
        return ApacData(
            patient_name = self.patient_name,
            patient_record_number = self.patient_record_number,
            patient_cns = self.patient_cns,
            patient_cpf = self.patient_cpf,
            patient_birth_date = self.patient_birth_date,
            patient_race_color = self.patient_race_color,
            patient_gender = self.patient_gender,
            patient_mother_name = self.patient_mother_name,
            patient_address_street_type = self.patient_address_street_type,
            patient_address_street_name = self.patient_address_street_name,
            patient_address_number = self.patient_address_number,
            patient_address_complement = self.patient_address_complement,
            patient_address_postal_code = self.patient_address_postal_code,
            patient_address_neighborhood = self.patient_address_neighborhood,
            patient_address_city = self.patient_address_city,
            patient_address_state = self.patient_address_state,
            medic_name = self.medic_name,
            medic_cns = self.medic_cns,
            medic_cbo = self.medic_cbo,
            cid=self.cid.to_entity(),
            procedure_date=self.procedure_date,
            main_procedure=self.main_procedure.to_entity(),
            sub_procedures=[record.to_entity() for record in records if record] if records else [],
            id=self.pk
        )
