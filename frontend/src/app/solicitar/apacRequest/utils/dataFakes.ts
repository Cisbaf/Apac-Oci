import { RequestForm } from "../schemas/requestForm";
import { fakeProcedureOne, subProcedures } from "@/shared/utils/procedureFakeList";

export const fakeRequestForm: RequestForm = {
    requesterId: 1,
    establishmentId: 2,
    requestDate: "2025-07-01",
    apacData: {
        patientName: "DANIEL FERNANDES PEREIRA",
        patientRecordNumber: "121212",
        patientCns: "701 8052 0927 4077",
        patientCpf: "187.149.337-48",
        patientBirthDate: "12/03/1999",
        patientRaceColor: "01",
        patientGender: "M",
        patientMotherName: "FERNANDA RODRIGUES FERNANDES",
        patientAddressStreetType: "081",
        patientAddressStreetName: "KATIA",
        patientAddressNumber: "200",
        patientAddressComplement: "CASA  LT",
        patientAddressPostalCode: "26261-360",
        patientAddressNeighborhood: "COMENDADOR SOARES",
        patientAddressCity: "Nova Iguaçu",
        patientAddressState: "RJ",
        supervisingPhysicianName: "ANA JULIA SANTOS DA SILVA",
        supervisingPhysicianCns: "706 0003 4345 8946",
        supervisingPhysicianCbo: "78956",
        authorizingPhysicianName: "DANIELLE ALVES DE CARVALHO",
        authorizingPhysicianCns: "705 8044 8124 3730",
        authorizingPhysicianCbo: "79654",
        cidId: 6,
        procedureDate: "01/08/2025",
        dischargeDate: "02/08/2025",
        mainProcedureId: 231,
        subProcedures: subProcedures
    }
};

export const fakeDataRequestFillingPart: RequestForm = {
  requesterId: 0,
  establishmentId: 0,
  requestDate: "",
  apacData: {
      patientName: "DANIEL FERNANDES PEREIRA",
      patientRecordNumber: "121212",
      patientCns: "701 8052 0927 4077",
      patientCpf: "187.149.337-48",
      patientBirthDate: "12/03/1999",
      patientRaceColor: "01",
      patientGender: "M",
      patientMotherName: "FERNANDA RODRIGUES FERNANDES",
      patientAddressStreetType: "081",
      patientAddressStreetName: "KATIA",
      patientAddressNumber: "200",
      patientAddressComplement: "CASA  LT",
      patientAddressPostalCode: "26261-360",
      patientAddressNeighborhood: "COMENDADOR SOARES",
      patientAddressCity: "Nova Iguaçu",
      patientAddressState: "RJ",
      supervisingPhysicianName: "ANA JULIA SANTOS DA SILVA",
      supervisingPhysicianCns: "706 0003 4345 8946",
      supervisingPhysicianCbo: "78956",
      authorizingPhysicianName: "DANIELLE ALVES DE CARVALHO",
      authorizingPhysicianCns: "705 8044 8124 3730",
      authorizingPhysicianCbo: "79654",
      cidId: 0,
      procedureDate: "01/08/2025",
      dischargeDate: "02/08/2025",
      mainProcedureId: 0,
      subProcedures: []
  }
};

