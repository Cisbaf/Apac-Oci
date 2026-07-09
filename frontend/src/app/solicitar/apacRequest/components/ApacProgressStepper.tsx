import React from "react";
import { ProgressStepper } from "@/shared/components/ProgressStepper";
import ConfirmDialog, { ConfirmDialogHandles } from "@/shared/components/ConfirmDialog";
import { useFormRequest } from "@/app/solicitar/apacRequest/contexts/FormApacRequest";
import { checkCepValidity, checkAgeProcedureAlert } from "@/app/solicitar/apacRequest/services/VerificationService";

// Índices (0-based) dos StepForm em page.tsx: 0=data da solicitação,
// 1=estabelecimento+paciente, 2=procedimento principal+sub-procedimentos.
const PATIENT_STEP_INDEX = 1;
const PROCEDURE_STEP_INDEX = 2;

interface ApacProgressStepperProps {
  children: React.ReactNode;
}

export default function ApacProgressStepper({ children }: ApacProgressStepperProps) {
  const { form } = useFormRequest();
  const confirmRef = React.useRef<ConfirmDialogHandles>(null);

  const handleBeforeNext = async (stepIndex: number): Promise<boolean> => {
    if (stepIndex === PATIENT_STEP_INDEX) {
      const cep = form.getValues("apacData.patientAddressPostalCode");
      const result = await checkCepValidity(cep);

      if (result.available && !result.valid) {
        const confirmed = await confirmRef.current?.confirm(
          "O CEP informado não foi encontrado na base dos Correios. Deseja continuar mesmo assim?"
        );
        return confirmed ?? true;
      }
      return true;
    }

    if (stepIndex === PROCEDURE_STEP_INDEX) {
      const birthDate = form.getValues("apacData.patientBirthDate");
      const procedureId = form.getValues("apacData.mainProcedureId");
      const result = await checkAgeProcedureAlert(birthDate, procedureId);

      if (result.available && result.alert) {
        const confirmed = await confirmRef.current?.confirm(
          result.message ||
            "Foi encontrado um alerta para a idade do paciente em relação ao procedimento selecionado. Deseja continuar mesmo assim?"
        );
        return confirmed ?? true;
      }
      return true;
    }

    return true;
  };

  return (
    <>
      <ProgressStepper onBeforeNext={handleBeforeNext}>{children}</ProgressStepper>
      <ConfirmDialog ref={confirmRef} />
    </>
  );
}
