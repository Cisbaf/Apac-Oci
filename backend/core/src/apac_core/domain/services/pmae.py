"""Regra PMAE — atributo complementar SIGTAP 053 (T-043).

O APAC Magnético recusa APAC de OCI com menos de dois procedimentos
secundários, e exige que um deles seja consulta ou teleconsulta:

    000013  PROC.PRINC(0908010010) PMAE EXIGE PELO MENOS 2 PROC.SEC.
            SENDO UM OBRIG.(030101007 OU 030101030)

**A regra não está em tabela nenhuma do SIGTAP.** Em `S_PAPA` a consulta é
secundário compatível (`PAPA_TRAT=01`) e `S_PADET` só marca que o
procedimento é PMAE (o código 053), sem dizer a quantidade nem quais códigos.
Ela vem da Portaria SAES/MS Nº 2.331/2024 e foi reproduzida no validador
oficial em 11/09/2026.

Até a T-042 isso era cadastrado OCI por OCI, como `ProcedureRequirementGroup`
— o que cobria "tem consulta" mas nunca "tem dois": seis OCIs aceitavam ser
enviadas só com a consulta, e as duas de Saúde Bucal, sem secundário nenhum.
Aqui a regra passa a ser derivada do atributo, e vale para toda OCI que o
tenha, inclusive as que ainda nem foram cadastradas.

A exigência da consulta é **condicional**: só vale se a OCI tiver consulta ou
teleconsulta entre os secundários que aceita. As duas OCIs de Saúde Bucal
(`0907010016`, `0907010024`) têm o atributo 053 mas não têm consulta médica em
`S_PAPA` — cobrá-la delas bloquearia a OCI inteira, sem ninguém conseguir
satisfazer. Para elas resta o mínimo de dois secundários, que é o que a
crítica cobra.
"""
from dataclasses import dataclass

#: Consulta Médica em Atenção Especializada e Teleconsulta Médica na Atenção
#: Especializada — os dois códigos que a crítica do APAC Magnético aceita.
CONSULTA = "0301010072"
TELECONSULTA = "0301010307"
CODIGOS_DE_CONSULTA = (CONSULTA, TELECONSULTA)

#: Mínimo de secundários que o APAC Magnético exige de um procedimento PMAE.
MINIMO_DE_SECUNDARIOS = 2


@dataclass(frozen=True)
class ViolacaoPmae:
    """O que está errado, na linguagem de quem preenche a APAC."""

    mensagem: str


def verificar(principal, codigos_marcados) -> ViolacaoPmae | None:
    """Devolve a violação da regra PMAE, ou `None` se o pacote está válido.

    `principal` é a entidade `Procedure` do procedimento principal (usa-se
    `pmae` e `sub_procedures`); `codigos_marcados` são os códigos SIGTAP dos
    secundários que o usuário marcou.
    """
    if not principal.pmae:
        return None

    marcados = list(codigos_marcados)
    if len(marcados) < MINIMO_DE_SECUNDARIOS:
        return ViolacaoPmae(
            f"Esta OCI exige pelo menos {MINIMO_DE_SECUNDARIOS} procedimentos "
            f"secundários; foi marcado {len(marcados)}."
        )

    aceita_consulta = {p.code for p in principal.sub_procedures} & set(CODIGOS_DE_CONSULTA)
    if aceita_consulta and not (set(marcados) & aceita_consulta):
        return ViolacaoPmae(
            "Esta OCI exige consulta médica em atenção especializada "
            f"({CONSULTA}) ou teleconsulta médica na atenção especializada "
            f"({TELECONSULTA}) entre os procedimentos secundários."
        )

    return None
