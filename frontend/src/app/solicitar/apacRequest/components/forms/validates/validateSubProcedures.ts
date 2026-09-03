import { RequirementGroup } from "@/shared/schemas/procedure";
import { SubProceduresForm } from "../../../schemas/requestForm";

export function validateSubProcedures(
  subProcedures: SubProceduresForm[],
  requirementGroups: RequirementGroup[] = []
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
