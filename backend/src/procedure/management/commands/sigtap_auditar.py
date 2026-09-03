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

from procedure.models import CidModel, ProcedureModel, ProcedureSecondary


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

    def _obter_ou_criar(self, model, codigo, nome, campo="code"):
        """`get_or_create` tolerante a código duplicado.

        `ProcedureModel.code` não tem constraint de unicidade e a produção tem
        duplicatas reais (mesmo código, grafias diferentes do nome — ex.:
        `0203020030` e `0301010307` em 03/09/2026). `get_or_create` levanta
        `MultipleObjectsReturned` nesses casos e aborta a auditoria inteira.
        Aqui a duplicata é avisada e resolvida pelo menor `id` — determinístico
        e inofensivo para o export, que grava o código, não o nome.
        """
        existentes = list(model.objects.filter(**{campo: codigo}).order_by("id"))
        if len(existentes) > 1:
            self.stdout.write(self.style.WARNING(
                f"    aviso: {codigo} está duplicado no cadastro "
                f"({len(existentes)}x, ids {[o.id for o in existentes]}) — "
                f"usando o id {existentes[0].id}. Vale limpar depois."))
        if existentes:
            return existentes[0]
        return model.objects.create(**{campo: codigo, "name": nome})

    def _auditar(self, d, aplicar):
        codigo = d["codigo_dv"]
        # order_by("id"): `code` não é único e a produção tem duplicatas — sem
        # ordenação explícita o `first()` não é determinístico no MySQL.
        principal = ProcedureModel.objects.filter(code=codigo).order_by("id").first()

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
        # oficiais: codigo_dv -> (obrigatório?, quantidade_maxima) — o par
        # decide os dois (T-037), não o procedimento.
        oficiais = {
            s["codigo_dv"]: (grupo == "obrigatorios", s["quantidade_maxima"])
            for grupo, lista in d["secundarios"].items()
            for s in lista
        }
        atuais = {
            link.child.code: link
            for link in ProcedureSecondary.objects.filter(parent=principal).select_related("child")
        }

        for codigo in sorted(set(oficiais) - set(atuais)):
            nome = next(
                s["nome"] for grupo in d["secundarios"].values() for s in grupo
                if s["codigo_dv"] == codigo
            )
            self._divergir(f"secundário ausente: {codigo} {nome[:44]}")
            if aplicar:
                obrigatorio, qtd_maxima = oficiais[codigo]
                sec = self._obter_ou_criar(ProcedureModel, codigo, nome)
                ProcedureSecondary.objects.create(
                    parent=principal, child=sec,
                    mandatory=obrigatorio, max_quantity=qtd_maxima)

        for codigo in sorted(set(atuais) - set(oficiais)):
            self._divergir(
                f"secundário que o SIGTAP não aceita para esta OCI: {codigo} "
                f"{atuais[codigo].child.name[:44]}")
            if aplicar:
                # Remove só o vínculo com o principal; o procedimento em si
                # continua existindo — pode ser secundário legítimo de outra OCI.
                atuais[codigo].delete()

        for codigo in sorted(set(oficiais) & set(atuais)):
            obrigatorio, qtd_maxima = oficiais[codigo]
            link = atuais[codigo]
            if link.mandatory != obrigatorio:
                self._divergir(
                    f"{codigo}: cadastrado como "
                    f"{'obrigatório' if link.mandatory else 'compatível'}, "
                    f"SIGTAP diz {'obrigatório' if obrigatorio else 'compatível'}")
                if aplicar:
                    link.mandatory = obrigatorio
                    link.save()
            if link.max_quantity != qtd_maxima:
                self._divergir(
                    f"{codigo}: quantidade máxima cadastrada "
                    f"{link.max_quantity}, SIGTAP diz {qtd_maxima}")
                if aplicar:
                    link.max_quantity = qtd_maxima
                    link.save()

    def _auditar_cids(self, principal, d, aplicar):
        oficiais = set(d["cids_principais"])
        atuais = {c.code: c for c in CidModel.objects.filter(procedure=principal)}

        for codigo in sorted(oficiais - set(atuais)):
            self._divergir(f"CID principal ausente: {codigo}")
            if aplicar:
                cid = self._obter_ou_criar(CidModel, codigo, codigo)
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
