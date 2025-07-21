import { ApacData } from "../schemas/apacRequest";
import { ApacData as ApacDataForm } from "../schemas/requestForm";

export function convertApacDataToForm(data: ApacData): ApacDataForm {
  return {
    patientName: data.patient_name,
    patientRecordNumber: data.patient_record_number,
    patientCns: data.patient_cns,
    patientCpf: data.patient_cpf,
    patientBirthDate: data.patient_birth_date,
    patientRaceColor: data.patient_race_color,
    patientGender: data.patient_gender,
    patientMotherName: data.patient_mother_name,
    patientAddressStreetType: data.patient_address_street_type,
    patientAddressStreetName: data.patient_address_street_name,
    patientAddressNumber: data.patient_address_number,
    patientAddressComplement: data.patient_address_complement,
    patientAddressPostalCode: data.patient_address_postal_code,
    patientAddressNeighborhood: data.patient_address_neighborhood,
    patientAddressCity: data.patient_address_city,
    patientAddressState: data.patient_address_state,
    medicName: data.medic_name,
    medicCns: data.medic_cns,
    medicCbo: data.medic_cbo,
    cidId: data.cid.id, // assumindo que Cid tem propriedade id do tipo number
    procedureDate: data.procedure_date,
    mainProcedureId: data.main_procedure.id, // assumindo que Procedure tem id
    subProcedures: data.sub_procedures.map(sp => ({
      procedure: sp.procedure,
      quantity: sp.quantity,
      checked: true,
    })),
  };
}
