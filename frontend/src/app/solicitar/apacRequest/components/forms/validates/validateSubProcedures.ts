import { SubProceduresForm } from "../../../schemas/requestForm";

export function validateSubProcedures(subProcedures: SubProceduresForm[]) {
  const mandatoryNotChecked = subProcedures.find(
    p => p.procedure.mandatory && !p.checked
  );

  if (mandatoryNotChecked) {
    return {
      success: false,
      message: `O procedimento obrigatório ${mandatoryNotChecked.procedure.name} não foi selecionado!`
    };
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
