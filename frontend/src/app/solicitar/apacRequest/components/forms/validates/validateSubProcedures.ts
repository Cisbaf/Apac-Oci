import Procedure, { RequirementGroup } from "@/shared/schemas/procedure";
import { SubProceduresForm } from "../../../schemas/requestForm";

// Atributo SIGTAP 053 (T-043). O APAC Magnético recusa OCI com menos de 2
// secundários e sem consulta:
//   "PMAE EXIGE PELO MENOS 2 PROC.SEC. SENDO UM OBRIG.(030101007 OU 030101030)"
export const CONSULTA = "0301010072";
export const TELECONSULTA = "0301010307";
const CODIGOS_DE_CONSULTA = [CONSULTA, TELECONSULTA];
const MINIMO_DE_SECUNDARIOS = 2;

/** Mensagem da regra PMAE violada, ou `null` se o pacote está válido.
 *
 * A exigência da consulta é condicional: só vale se a OCI aceitar consulta ou
 * teleconsulta entre seus secundários. As duas OCIs de Saúde Bucal têm o
 * atributo 053 mas não têm consulta médica no SIGTAP — cobrá-la delas
 * bloquearia a OCI inteira, sem ninguém conseguir satisfazer. */
export function validatePmae(
  marcados: SubProceduresForm[],
  mainProcedure?: Procedure
): string | null {
  if (!mainProcedure?.pmae) return null;

  if (marcados.length < MINIMO_DE_SECUNDARIOS) {
    return `Esta OCI exige pelo menos ${MINIMO_DE_SECUNDARIOS} procedimentos secundários; foi marcado ${marcados.length}.`;
  }

  const aceitaConsulta = (mainProcedure.children ?? [])
    .map(c => c.code)
    .filter(code => CODIGOS_DE_CONSULTA.includes(code));

  if (aceitaConsulta.length === 0) return null;

  const temConsulta = marcados.some(p => aceitaConsulta.includes(p.procedure.code));
  if (!temConsulta) {
    return `Esta OCI exige consulta médica em atenção especializada (${CONSULTA}) ou teleconsulta médica na atenção especializada (${TELECONSULTA}) entre os procedimentos secundários.`;
  }

  return null;
}

export function validateSubProcedures(
  subProcedures: SubProceduresForm[],
  requirementGroups: RequirementGroup[] = [],
  mainProcedure?: Procedure
) {
  const mandatoryNotChecked = subProcedures.find(
    p => p.procedure.mandatory && !p.checked
  );

  if (mandatoryNotChecked) {
    return {
      success: false,
      message: `O procedimento obrigatório ${mandatoryNotChecked.procedure.name} não foi selecionado!`
    };
  }

  // "Exige ao menos N destes M" (atributos SIGTAP 057/067-070, T-040) — não é
  // um item obrigatório sozinho, é uma alternativa entre vários.
  for (const group of requirementGroups) {
    const marcados = subProcedures.filter(
      p => p.checked && group.member_ids.includes(p.procedure.id)
    ).length;
    if (marcados < group.minimum) {
      return {
        success: false,
        message: `Este procedimento exige pelo menos ${group.minimum} de: ${group.description}`
      };
    }
  }

  const violacaoPmae = validatePmae(subProcedures.filter(p => p.checked), mainProcedure);
  if (violacaoPmae) {
    return { success: false, message: violacaoPmae };
  }

  const incorrectQuantity = subProcedures.find(
    p => p.checked && (!p.quantity || p.quantity <= 0)
  );

  if (incorrectQuantity) {
    return {
      success: false,
      message: `Defina a quantidade para o procedimento ${incorrectQuantity.procedure.name}`
    };
  }

  return { success: true, message: "ok" };
}
