"""Semeia os CIDs de causas associadas (atributo SIGTAP 043) nas OCIs que os exigem.

O SIGTAP não guarda essa lista — o atributo 043 diz "este procedimento exige um
segundo CID", mas quais CIDs são aceitos como esse segundo CID vem do texto da
portaria, não de uma tabela. Por isso este comando lê o JSON preservado na
T-035 (`scripts/sigtap/cids_causas_associadas.json`, transcrito da Portaria
SAES/MS Nº 4.306/2026) em vez de extrair de `ambientes/<competencia>/`.

    python manage.py sigtap_semear_cid_secundario \
        --json ../../scripts/sigtap/cids_causas_associadas.json

    python manage.py sigtap_semear_cid_secundario --json ... --aplicar
"""
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from procedure.models import CidModel, ProcedureModel


class Command(BaseCommand):
    help = "Semeia os CIDs de causas associadas (atributo 043) e marca requires_secondary_cid"

    def add_arguments(self, parser):
        parser.add_argument("--json", required=True,
                            help="scripts/sigtap/cids_causas_associadas.json (T-035)")
        parser.add_argument("--aplicar", action="store_true",
                            help="grava; sem isto só relata")

    def handle(self, *args, **opts):
        with open(opts["json"]) as f:
            dados = json.load(f)

        self.mudancas = 0
        with transaction.atomic():
            for codigo, info in dados.items():
                self._semear(codigo, info, opts["aplicar"])
            if not opts["aplicar"]:
                transaction.set_rollback(True)

        self.stdout.write("")
        if opts["aplicar"]:
            self.stdout.write(self.style.SUCCESS(f"{self.mudancas} mudança(s) gravada(s)."))
        else:
            self.stdout.write(self.style.WARNING(
                f"{self.mudancas} mudança(s) pendente(s). Rode com --aplicar para gravar."))

    def _semear(self, codigo, info, aplicar):
        # order_by("id"): `code` não tem constraint de unicidade e a produção
        # tem duplicatas reais — sem ordenação o `first()` é não-determinístico.
        principal = ProcedureModel.objects.filter(code=codigo).order_by("id").first()
        if principal is None:
            self.stdout.write(self.style.WARNING(
                f"  ! {codigo}: procedimento não cadastrado — rode sigtap_auditar antes"))
            return

        self.stdout.write(f"\n{codigo} {info['nome'][:56]}")

        if not principal.requires_secondary_cid:
            self.mudancas += 1
            self.stdout.write("  ! requires_secondary_cid ausente")
            if aplicar:
                principal.requires_secondary_cid = True
                principal.save()

        atuais = {c.code for c in CidModel.objects.filter(secondary_of_procedure=principal)}
        oficiais = {c["codigo"]: c["nome"] for c in info["cids_causas_associadas"]}

        for codigo_cid in sorted(set(oficiais) - atuais):
            self.mudancas += 1
            self.stdout.write(f"  ! CID de causas associadas ausente: {codigo_cid}")
            if aplicar:
                cid = (CidModel.objects.filter(code=codigo_cid).order_by("id").first()
                       or CidModel.objects.create(
                           code=codigo_cid, name=oficiais[codigo_cid]))
                cid.secondary_of_procedure.add(principal)

        for codigo_cid in sorted(atuais - set(oficiais)):
            self.mudancas += 1
            self.stdout.write(
                f"  ! CID de causas associadas cadastrado que a portaria não lista: {codigo_cid}")
            if aplicar:
                for cid in CidModel.objects.filter(code=codigo_cid):
                    cid.secondary_of_procedure.remove(principal)
