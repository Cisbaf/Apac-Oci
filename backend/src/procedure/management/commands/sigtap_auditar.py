"""Compara o cadastro de procedimentos do sistema com a verdade oficial do SIGTAP.

O JSON de entrada é o produzido por `scripts/sigtap/extrair.py`, que lê as tabelas
DBF da competência montada pelo apac-magnetico-validador — as mesmas tabelas que o
APAC Magnético usa para criticar o arquivo. Divergência apontada aqui é crítica
que o município tomaria na hora de faturar.

    # 1. extrair a verdade oficial
    python3 scripts/sigtap/extrair.py .../ambientes/202608a --grupo 0907 0908 \
        --json /tmp/ocis.json

    # 2. conferir (não escreve nada)
    python manage.py sigtap_auditar --json /tmp/ocis.json

    # 3. corrigir o cadastro
    python manage.py sigtap_auditar --json /tmp/ocis.json --aplicar
"""
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from procedure.models import CidModel, ProcedureModel


class Command(BaseCommand):
    help = "Audita (e opcionalmente corrige) o cadastro de procedimentos contra o SIGTAP"

    def add_arguments(self, parser):
        parser.add_argument("--json", required=True,
                            help="JSON gerado por scripts/sigtap/extrair.py")
        parser.add_argument("--aplicar", action="store_true",
                            help="grava as correções; sem isto só relata")

    def handle(self, *args, **opts):
        with open(opts["json"]) as f:
            sigtap = json.load(f)

        self.divergencias = 0
        with transaction.atomic():
            for dados in sigtap.values():
                self._auditar(dados, opts["aplicar"])
            if not opts["aplicar"]:
                transaction.set_rollback(True)

        self.stdout.write("")
        if not self.divergencias:
            self.stdout.write(self.style.SUCCESS(
                "Cadastro conforme o SIGTAP — nenhuma divergência."))
        elif opts["aplicar"]:
            self.stdout.write(self.style.SUCCESS(
                f"{self.divergencias} divergência(s) corrigida(s)."))
        else:
            self.stdout.write(self.style.WARNING(
                f"{self.divergencias} divergência(s). Rode com --aplicar para corrigir."))

    # ------------------------------------------------------------------

    def _auditar(self, d, aplicar):
        codigo = d["codigo_dv"]
        principal = ProcedureModel.objects.filter(code=codigo).first()

        self.stdout.write(f"\n{codigo} {d['nome'][:56]}")
        if principal is None:
            self._divergir(f"procedimento principal não cadastrado no sistema")
            if aplicar:
                principal = ProcedureModel.objects.create(code=codigo, name=d["nome"])
                self.stdout.write(self.style.SUCCESS("    criado"))
            else:
                return

        self._auditar_secundarios(principal, d, aplicar)
        self._auditar_cids(principal, d, aplicar)

    def _auditar_secundarios(self, principal, d, aplicar):
        oficiais = {s["codigo_dv"]: s for grupo in d["secundarios"].values()
                    for s in grupo}
        atuais = {p.code: p for p in ProcedureModel.objects.filter(parents=principal)}

        for codigo in sorted(set(oficiais) - set(atuais)):
            self._divergir(f"secundário ausente: {codigo} {oficiais[codigo]['nome'][:44]}")
            if aplicar:
                sec, _ = ProcedureModel.objects.get_or_create(
                    code=codigo, defaults={"name": oficiais[codigo]["nome"]})
                sec.parents.add(principal)

        for codigo in sorted(set(atuais) - set(oficiais)):
            self._divergir(
                f"secundário que o SIGTAP não aceita para esta OCI: {codigo} "
                f"{atuais[codigo].name[:44]}")
            if aplicar:
                # Desvincula do principal; o procedimento em si continua existindo
                # porque pode ser secundário legítimo de outra OCI.
                atuais[codigo].parents.remove(principal)

    def _auditar_cids(self, principal, d, aplicar):
        oficiais = set(d["cids_principais"])
        atuais = {c.code: c for c in CidModel.objects.filter(procedure=principal)}

        for codigo in sorted(oficiais - set(atuais)):
            self._divergir(f"CID principal ausente: {codigo}")
            if aplicar:
                cid, _ = CidModel.objects.get_or_create(
                    code=codigo, defaults={"name": codigo})
                cid.procedure.add(principal)

        for codigo in sorted(set(atuais) - oficiais):
            self._divergir(
                f"CID vinculado que o SIGTAP não aceita como principal: {codigo}")
            if aplicar:
                # Não apaga o CID: ele volta a ser vinculado como CID de causas
                # associadas quando a T-036 criar esse campo.
                atuais[codigo].procedure.remove(principal)

    def _divergir(self, mensagem):
        self.divergencias += 1
        self.stdout.write(self.style.WARNING(f"  ! {mensagem}"))
