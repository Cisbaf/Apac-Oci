import { ApacData } from "../schemas/apacRequest";
import { ApacData as ApacDataForm } from "../schemas/requestForm";
import { applyMask, CnsMask, CpfMask, CepMask } from "@/shared/utils/mask";
import { formatDateBr } from "./adapterForm";

export function convertApacDataToForm(data: ApacData): ApacDataForm {
  return {
    patientName: data.patient_data.name,
    patientRecordNumber: data.patient_data.record_number,
    patientCns: applyMask(data.patient_data.cns, CnsMask),
    patientCpf: applyMask(data.patient_data.cpf, CpfMask),
    patientBirthDate: formatDateBr(data.patient_data.birth_date),
    patientRaceColor: data.patient_data.race_color,
    patientGender: data.patient_data.gender,
    patientMotherName: data.patient_data.mother_name,
    patientAddressStreetType: data.patient_data.address_street_type,
    patientAddressStreetName: data.patient_data.address_street_name,
    patientAddressNumber: data.patient_data.address_number,
    patientAddressComplement: data.patient_data.address_complement,
    patientAddressPostalCode: applyMask(data.patient_data.address_postal_code, CepMask),
    patientAddressNeighborhood: data.patient_data.address_neighborhood,
    patientAddressCity: data.patient_data.address_city,
    patientAddressState: data.patient_data.address_state,
    supervisingPhysicianName: data.supervising_physician_data.name,
    supervisingPhysicianCns: applyMask(data.supervising_physician_data.cns, CnsMask),
    supervisingPhysicianCbo: data.supervising_physician_data.cbo,
    authorizingPhysicianName: data.authorizing_physician_data.name,
    authorizingPhysicianCns: applyMask(data.authorizing_physician_data.cns, CnsMask),
    authorizingPhysicianCbo: data.authorizing_physician_data.cbo,
    cidId: data.cid.id, // assumindo que Cid tem propriedade id do tipo number
    procedureDate: formatDateBr(data.procedure_date),
    dischargeDate: formatDateBr(data.discharge_date),
    mainProcedureId: data.main_procedure.id, // assumindo que Procedure tem id
    subProcedures: data.sub_procedures.map(sp => ({
      procedure: sp.procedure,
      quantity: sp.quantity,
      checked: true,
    })),
  };
}
