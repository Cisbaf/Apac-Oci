import { formatDateToISO } from "../utils/adapterForm";

export interface CepCheckResult {
  available: boolean;
  valid: boolean;
}

/**
 * Consulta o ViaCEP para checar se o CEP informado existe. Falhas de rede ou
 * de indisponibilidade do serviço resultam em `available: false` para que o
 * chamador não bloqueie o usuário quando a verificação não puder ser feita.
 */
export async function checkCepValidity(cep: string): Promise<CepCheckResult> {
  const digits = (cep || "").replace(/\D/g, "");
  if (digits.length !== 8) {
    return { available: true, valid: false };
  }

  try {
    const response = await fetch(`https://viacep.com.br/ws/${digits}/json/`);
    if (!response.ok) {
      return { available: false, valid: true };
    }
    const data = await response.json();
    return { available: true, valid: !data.erro };
  } catch {
    return { available: false, valid: true };
  }
}

export interface AgeProcedureAlertResult {
  available: boolean;
  alert: boolean;
  message?: string;
}

/**
 * Checa, via backend, se existe algum alerta para a combinação de idade do
 * paciente e procedimento selecionado. Indisponibilidade da API resulta em
 * `available: false`, permitindo que o formulário prossiga normalmente.
 */
export async function checkAgeProcedureAlert(
  birthDate: string,
  procedureId: number
): Promise<AgeProcedureAlertResult> {
  if (!procedureId || !birthDate || birthDate.length !== 10) {
    return { available: true, alert: false };
  }

  try {
    const response = await fetch("/api/proxy/procedure/apac/check-age-alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        procedure_id: procedureId,
        birth_date: formatDateToISO(birthDate),
      }),
    });

    if (!response.ok) {
      return { available: false, alert: false };
    }

    const data = await response.json();
    return { available: true, alert: Boolean(data.alert), message: data.message };
  } catch {
    return { available: false, alert: false };
  }
}
