"""T-043 — regra PMAE (atributo SIGTAP 053) como função pura.

Os casos vêm do que o APAC Magnético devolveu de verdade no validador oficial
(ambiente 202608a, 11/09/2026) para a OCI `0908010010`:

| secundários marcados                | veredito do programa |
|-------------------------------------|----------------------|
| TC de tórax + consulta              | SEM ERROS            |
| TC de tórax + teleconsulta          | SEM ERROS            |
| TC de tórax + baciloscopia          | crítica 000013 PMAE  |
| só a TC de tórax                    | crítica 000013 PMAE  |
"""
from apac_core.domain.entities.procedure import Procedure
from apac_core.domain.services import pmae

TOMOGRAFIA = "0206020031"
BACILOSCOPIA = "0202080048"
BIOPSIA_DE_PELE = "0201010372"


def oci(*codigos_de_secundarios, com_atributo=True):
    return Procedure(
        name="OCI de teste",
        code="0908010010",
        pmae=com_atributo,
        sub_procedures=[
            Procedure(name=f"Secundário {c}", code=c) for c in codigos_de_secundarios
        ],
    )


class TestRegraPmae:

    def test_procedimento_sem_o_atributo_nao_e_afetado(self):
        principal = oci(TOMOGRAFIA, pmae.CONSULTA, com_atributo=False)

        assert pmae.verificar(principal, [TOMOGRAFIA]) is None

    def test_um_secundario_so_nao_basta(self):
        principal = oci(TOMOGRAFIA, pmae.CONSULTA, pmae.TELECONSULTA)

        violacao = pmae.verificar(principal, [TOMOGRAFIA])

        assert violacao is not None
        assert "pelo menos 2" in violacao.mensagem

    def test_nem_a_consulta_sozinha_basta(self):
        """Seis OCIs em produção aceitavam exatamente isto antes da T-043."""
        principal = oci(TOMOGRAFIA, pmae.CONSULTA, pmae.TELECONSULTA)

        violacao = pmae.verificar(principal, [pmae.CONSULTA])

        assert violacao is not None
        assert "pelo menos 2" in violacao.mensagem

    def test_dois_secundarios_sem_consulta_nao_passam(self):
        principal = oci(TOMOGRAFIA, BACILOSCOPIA, pmae.CONSULTA, pmae.TELECONSULTA)

        violacao = pmae.verificar(principal, [TOMOGRAFIA, BACILOSCOPIA])

        assert violacao is not None
        assert pmae.CONSULTA in violacao.mensagem

    def test_tomografia_mais_consulta_passa(self):
        principal = oci(TOMOGRAFIA, pmae.CONSULTA, pmae.TELECONSULTA)

        assert pmae.verificar(principal, [TOMOGRAFIA, pmae.CONSULTA]) is None

    def test_teleconsulta_serve_no_lugar_da_consulta(self):
        principal = oci(TOMOGRAFIA, pmae.CONSULTA, pmae.TELECONSULTA)

        assert pmae.verificar(principal, [TOMOGRAFIA, pmae.TELECONSULTA]) is None

    def test_oci_que_nao_aceita_consulta_so_precisa_dos_dois_secundarios(self):
        """Saúde Bucal (`0907010016`, `0907010024`): têm o atributo 053 mas não
        têm consulta médica em `S_PAPA`. Cobrar consulta delas bloquearia a OCI
        inteira — nenhum secundário disponível satisfaria a regra."""
        principal = oci(BIOPSIA_DE_PELE, BACILOSCOPIA)

        assert pmae.verificar(principal, [BIOPSIA_DE_PELE, BACILOSCOPIA]) is None

    def test_oci_que_nao_aceita_consulta_ainda_exige_dois(self):
        principal = oci(BIOPSIA_DE_PELE, BACILOSCOPIA)

        violacao = pmae.verificar(principal, [BIOPSIA_DE_PELE])

        assert violacao is not None
        assert "pelo menos 2" in violacao.mensagem
