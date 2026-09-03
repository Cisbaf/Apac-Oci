"""Semeia os grupos de exigência alternativa (atributos SIGTAP 057, 067-070...).

O SIGTAP não guarda em nenhuma tabela "este procedimento aceita 1 destes N" —
só marca, em S_PADET, que a regra existe (o código do atributo). Confirmado
nesta tarefa: nem S_PAREGR (regras genéricas, iguais nas 8 OCIs) nem
S_PAPA.PAPA_TRAT 98/99 (que é exclusão mútua, um assunto diferente) carregam
essa lista. A lista em si vem do texto oficial da Portaria SAES/MS Nº
4.306/2026 (atributos 067-070) e da wiki do SIGTAP (atributo 057, pré-
existente) — preservada em `scripts/sigtap/grupos_exigencia.json`.

Todo membro de todo grupo aqui já existe como secundário compatível da OCI
(confirmado contra S_PAPA antes de escrever o JSON) — este comando não
cadastra procedimento novo, só a regra de "pelo menos N" em cima do que já
está linkado.

    python manage.py sigtap_semear_grupos_exigencia \
        --json ../../scripts/sigtap/grupos_exigencia.json

    python manage.py sigtap_semear_grupos_exigencia --json ... --aplicar
"""
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from procedure.models import ProcedureModel, ProcedureRequirementGroup


class Command(BaseCommand):
    help = "Semeia os grupos de exigência alternativa (atributos 057, 067-070...)"

    def add_arguments(self, parser):
        parser.add_argument("--json", required=True,
                            help="scripts/sigtap/grupos_exigencia.json")
        parser.add_argument("--aplicar", action="store_true",
                            help="grava; sem isto só relata")

    def handle(self, *args, **opts):
        with open(opts["json"]) as f:
            dados = json.load(f)

        self.mudancas = 0
        with transaction.atomic():
            for chave, info in dados.items():
                if chave.startswith("_"):
                    continue
                self._semear(info, opts["aplicar"])
            if not opts["aplicar"]:
                transaction.set_rollback(True)

        self.stdout.write("")
        if opts["aplicar"]:
            self.stdout.write(self.style.SUCCESS(f"{self.mudancas} mudança(s) gravada(s)."))
        else:
            self.stdout.write(self.style.WARNING(
                f"{self.mudancas} mudança(s) pendente(s). Rode com --aplicar para gravar."))

    def _semear(self, info, aplicar):
        codigo = info["codigo_dv"]
        principal = ProcedureModel.objects.filter(code=codigo).first()
        if principal is None:
            self.stdout.write(self.style.WARNING(
                f"  ! {codigo}: procedimento não cadastrado — rode sigtap_auditar antes"))
            return

        self.stdout.write(f"\n{codigo} {info['nome'][:56]} (atributo {info['attribute_code']})")

        membros_oficiais = self._resolver_membros(principal, info)
        if not membros_oficiais:
            self.stdout.write(self.style.WARNING(
                "  ! nenhum membro resolvido — confira subgroup_prefixes/members no JSON"))
            return

        grupo = ProcedureRequirementGroup.objects.filter(
            principal=principal, attribute_code=info["attribute_code"]).first()

        if grupo is None:
            self.mudancas += 1
            self.stdout.write(f"  ! grupo ausente ({len(membros_oficiais)} membros)")
            if aplicar:
                grupo = ProcedureRequirementGroup.objects.create(
                    principal=principal, attribute_code=info["attribute_code"],
                    description=info["description"], minimum=info["minimum"])
                grupo.members.set(membros_oficiais)
            return

        if grupo.description != info["description"] or grupo.minimum != info["minimum"]:
            self.mudancas += 1
            self.stdout.write("  ! descrição ou mínimo divergente")
            if aplicar:
                grupo.description = info["description"]
                grupo.minimum = info["minimum"]
                grupo.save()

        atuais = set(grupo.members.values_list("id", flat=True))
        oficiais_ids = {p.id for p in membros_oficiais}
        if atuais != oficiais_ids:
            self.mudancas += 1
            self.stdout.write(
                f"  ! membros divergentes: cadastrado={len(atuais)} oficial={len(oficiais_ids)}")
            if aplicar:
                grupo.members.set(membros_oficiais)

    def _resolver_membros(self, principal, info):
        """Códigos fixos (`members`) ou por prefixo de subgrupo dentre os
        secundários já compatíveis com este principal (`subgroup_prefixes`)."""
        if "members" in info:
            return list(ProcedureModel.objects.filter(code__in=info["members"]))

        prefixos = tuple(info["subgroup_prefixes"])
        candidatos = [
            link.child for link in principal.secondary_links.select_related("child")
            if link.child.code[:9][:4] in prefixos
        ]
        return candidatos
