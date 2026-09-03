# T-037: copia o M2M "parents" (par principal×secundário) para o modelo
# explícito ProcedureSecondary antes de removê-lo (migration 0029). O valor
# inicial de `mandatory` é herdado do antigo ProcedureModel.mandatory — o
# melhor sinal disponível até o sigtap_auditar corrigir por par; `max_quantity`
# nasce vazio (o cadastro manual nunca guardou essa informação).
from django.db import migrations


def copiar(apps, schema_editor):
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureSecondary = apps.get_model("procedure", "ProcedureSecondary")

    for filho in ProcedureModel.objects.prefetch_related("parents").all():
        for principal in filho.parents.all():
            ProcedureSecondary.objects.get_or_create(
                parent=principal,
                child=filho,
                defaults={"mandatory": filho.mandatory, "max_quantity": None},
            )


def reverter(apps, schema_editor):
    """Restaura o M2M `parents` E o booleano `mandatory` do procedimento.

    Restaurar só o vínculo perderia silenciosamente as marcações de
    obrigatoriedade (em produção, 16 procedimentos com `mandatory=True`) — o
    rollback ficaria verde mas com dado a menos. Como o `mandatory` do modelo
    antigo era do procedimento e o novo é do par, a reconstrução possível é:
    o filho volta a ser obrigatório se QUALQUER vínculo dele era obrigatório.
    É exatamente o inverso do `copiar`, que propagou o valor do filho para
    todos os pares dele.
    """
    ProcedureModel = apps.get_model("procedure", "ProcedureModel")
    ProcedureSecondary = apps.get_model("procedure", "ProcedureSecondary")

    obrigatorios = set()
    for link in ProcedureSecondary.objects.select_related("child", "parent"):
        link.child.parents.add(link.parent)
        if link.mandatory:
            obrigatorios.add(link.child_id)

    if obrigatorios:
        ProcedureModel.objects.filter(pk__in=obrigatorios).update(mandatory=True)


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0027_proceduresecondary'),
    ]

    operations = [
        migrations.RunPython(copiar, reverter),
    ]
