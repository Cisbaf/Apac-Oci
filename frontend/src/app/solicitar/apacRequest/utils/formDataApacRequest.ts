import { RequestForm } from "../schemas/requestForm";

// Empty RequestForm
export const emptyRequestForm: RequestForm = {
  requesterId: 0,
  establishmentId: 0,
  apacData: {
    patientName: "",
    patientRecordNumber: "",
    patientCns: "",
    patientCpf: "",
    patientBirthDate: "",
    patientRaceColor: "",
    patientGender: "",
    patientMotherName: "",
    patientAddressStreetType: "",
    patientAddressStreetName: "",
    patientAddressNumber: "",
    patientAddressComplement: "",
    patientAddressPostalCode: "",
    patientAddressNeighborhood: "",
    patientAddressCity: "",
    patientAddressState: "",
    supervisingPhysicianName: "",
    supervisingPhysicianCns: "",
    supervisingPhysicianCbo: "",
    authorizingPhysicianName: "",
    authorizingPhysicianCns: "",
    authorizingPhysicianCbo: "",
    cidId: 0,
    procedureDate: "",
    dischargeDate: "",
    mainProcedureId: 0,
    subProcedures: []
  }
};
