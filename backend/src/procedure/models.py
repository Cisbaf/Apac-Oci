from django.db import models
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.entities.cid import Cid


class ProcedureModel(models.Model):
    code = models.CharField(verbose_name="Código do Procedimento", max_length=20, db_column='cod_sig_tap')
    name = models.CharField(verbose_name="Nome do Procedimento", max_length=255)
    description = models.CharField(verbose_name="Descrição do Procedimento", max_length=255, null=True, blank=True)
    # Atributo complementar SIGTAP 054. Ver T-034: a validade padrão da APAC é de
    # 3 competências (Portaria SAES/MS Nº 3.958/2026), mas procedimentos que ainda
    # carregam o 054 são rejeitados pelo APAC Magnético com o erro 010087 se
    # exportados com validade diferente de 2 competências.
    fixed_validity_two_competences = models.BooleanField(
        verbose_name="Validade fixa de 2 competências",
        help_text="Atributo SIGTAP 054. Marque se o APAC Magnético exigir validade de 2 competências para este procedimento (erro 010087). Sem marcar, a validade exportada é a padrão de 3 competências.",
        default=False
    )
    is_active = models.BooleanField(verbose_name="Está ativo", default=True)
    # Atributo complementar SIGTAP 043. Ver T-036: procedimentos com este atributo
    # (as 8 OCIs de Infectologia da Portaria SAES/MS Nº 4.306/2026) exigem, além do
    # CID principal, um segundo CID — o da síndrome associada ao HIV/aids que
    # motivou o atendimento. Sem ele o APAC Magnético rejeita a APAC com
    # "EXIGE CID CAUSAS ASSOC.CONF.PT/GM 584 DE 15/5/15".
    requires_secondary_cid = models.BooleanField(
        verbose_name="Exige CID de causas associadas",
        help_text="Atributo SIGTAP 043. Marque se o APAC Magnético exigir um segundo CID (causas associadas) para este procedimento.",
        default=False
    )
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
            sub_procedures = [
                link.child.to_entity(**kwargs)
                for link in self.secondary_links.select_related("child")
            ]

        return Procedure (
            name=self.name,
            code=self.code,
            description=self.description,
            is_active=self.is_active,
            fixed_validity_two_competences=self.fixed_validity_two_competences,
            requires_secondary_cid=self.requires_secondary_cid,
            sub_procedures=sub_procedures,
            created_at=self.created_at,
            updated_at=self.updated_at,
            id=self.pk
        )

    def __str__(self):
        return self.name


class ProcedureSecondary(models.Model):
    """Vínculo principal×secundário (T-037).

    O SIGTAP guarda "obrigatório" e "quantidade máxima" no *par*
    (`S_PAPA.PAPA_TRAT`/`PAPA_QTMAX`), não no procedimento — mas o cadastro
    manual guardava `mandatory` como atributo do `ProcedureModel`, sem como
    expressar que um secundário é obrigatório numa OCI e só compatível noutra
    (achado da T-035: 6 secundários com papel divergente entre as 10 OCIs
    novas, 5 com quantidade divergente). Este modelo substitui o M2M simples
    `ProcedureModel.parents` para guardar essa informação por par.
    """
    parent = models.ForeignKey(
        to="ProcedureModel", on_delete=models.CASCADE,
        related_name="secondary_links", verbose_name="Procedimento principal"
    )
    child = models.ForeignKey(
        to="ProcedureModel", on_delete=models.CASCADE,
        related_name="parent_links", verbose_name="Procedimento secundário"
    )
    mandatory = models.BooleanField(verbose_name="Obrigatório", default=False)
    max_quantity = models.PositiveIntegerField(
        verbose_name="Quantidade máxima",
        help_text="Atributo SIGTAP PAPA_QTMAX. Vazio = sem limite conhecido cadastrado.",
        null=True, blank=True
    )

    class Meta:
        db_table = 'procedimentos_secundarios'
        unique_together = ("parent", "child")
        verbose_name = "Procedimento secundário"
        verbose_name_plural = "Procedimentos secundários"

    def __str__(self):
        return f"{self.parent.code} → {self.child.code}"


class CidModel(models.Model):
    code = models.CharField(verbose_name="Código CID", max_length=20, db_column='cod_cid')
    name = models.CharField(verbose_name="Nome CID", max_length=255)

    procedure = models.ManyToManyField(
        to=ProcedureModel,
        symmetrical=False,
        related_name="cids",
        blank=True
    )
    # CID de causas associadas (atributo SIGTAP 043, ver T-036): procedimentos
    # cujo cadastro aceita este CID como o *segundo* CID (a síndrome associada),
    # não como o principal. Vínculo separado do M2M acima de propósito — é
    # exatamente misturar os dois papéis num só vínculo que fez o cadastro
    # manual escolher um CID secundário como se fosse principal (ver T-035).
    secondary_of_procedure = models.ManyToManyField(
        to=ProcedureModel,
        symmetrical=False,
        related_name="secondary_cids",
        blank=True
    )
    is_active = models.BooleanField(verbose_name="Está ativo", default=True)

    def to_entity(self, **kwargs):
        exclude = kwargs.get("exclude_cid_procedures", None)
        procedures = []
        if not exclude:
            procedures = [children.to_entity(**kwargs) for children in ProcedureModel.objects.filter(cids=self)]
        return Cid(
            code=self.code,
            name=self.name,
            procedure=None if exclude else procedures,
            id=self.pk
        )

    class Meta:
        db_table = 'cid'
        verbose_name = "Cid"
        verbose_name_plural = "Cids"

    def __str__(self):
        return f"{self.code} - {self.name}"