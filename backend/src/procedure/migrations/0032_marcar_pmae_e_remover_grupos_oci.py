# T-043: liga a regra PMAE (atributo SIGTAP 053) nas OCIs já cadastradas e
# recolhe o mecanismo anterior, que era cadastrar a consulta obrigatória como
# `ProcedureRequirementGroup` OCI por OCI (T-042 e antes dela, GIN3/orofaringe/
# gástrico).
#
# Por que dá para marcar por prefixo: o grupo 09 do SIGTAP é o das OCIs, e
# todas as 46 OCIs da competência 202608a têm o atributo 053 — conferido na
# S_PADET. Em produção, os 31 procedimentos com código 09* são exatamente as 31
# OCIs cadastradas; nenhum secundário cai nesse prefixo.
#
# Os grupos OCI ficam redundantes a partir daqui: a regra derivada cobre "tem
# consulta" e ainda cobre "tem pelo menos 2 secundários", que o grupo nunca
# cobriu — eram 8 OCIs aceitando envio que o SIA critica, seis delas só com a
# consulta. Manter os dois faria o formulário dizer a mesma coisa duas vezes.
from django.db import migrations

#: Os 11 principais que tinham o grupo OCI quando esta migration foi escrita
#: (11/09/2026). Lista explícita porque o `reverse` precisa recriar exatamente
#: esses — deduzir por "tem consulta entre os secundários" traria junto as 20
#: OCIs que resolvem a mesma regra por `ProcedureSecondary.mandatory`, que
#: nunca tiveram grupo.
PRINCIPAIS_COM_GRUPO_OCI = [
    "0901010073", "0904010031", "0906010055",
    "0908010010", "0908010028", "0908010036", "0908010044",
    "0908010052", "0908010060", "0908010079", "0908010087",
]

CODIGOS_DE_CONSULTA = ["0301010072", "0301010307"]

DESCRICAO = ("Consulta médica em atenção especializada ou teleconsulta médica na "
             "atenção especializada (toda APAC de OCI exige uma das duas)")


def aplicar(apps, schema_editor):
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureRequirementGroup = apps.get_model("procedure", "ProcedureRequirementGroup")

    ProcedureModel.objects.filter(code__startswith="09").update(pmae=True)
    ProcedureRequirementGroup.objects.filter(attribute_code="OCI").delete()


def reverter(apps, schema_editor):
    """Desmarca o atributo e recria os grupos OCI com os membros que cada
    principal aceita — `0904010031` e `0908010044` voltam com só a consulta,
    porque o SIGTAP não lista teleconsulta como secundário delas.

    A descrição recriada é a padrão: as três OCIs anteriores à T-042 tinham um
    texto ligeiramente diferente, e essa diferença de redação não vale o
    trabalho de preservar.
    """
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureRequirementGroup = apps.get_model("procedure", "ProcedureRequirementGroup")

    ProcedureModel.objects.filter(code__startswith="09").update(pmae=False)

    for code in PRINCIPAIS_COM_GRUPO_OCI:
        principal = ProcedureModel.objects.filter(code=code).first()
        if principal is None:
            continue
        membros = [
            link.child for link in principal.secondary_links.select_related("child")
            if link.child.code in CODIGOS_DE_CONSULTA
        ]
        if not membros:
            continue
        grupo = ProcedureRequirementGroup.objects.create(
            principal=principal, attribute_code="OCI",
            description=DESCRICAO, minimum=1,
        )
        grupo.members.set(membros)


class Migration(migrations.Migration):

    dependencies = [
        ("procedure", "0031_proceduremodel_pmae"),
    ]

    operations = [
        migrations.RunPython(aplicar, reverter),
    ]
