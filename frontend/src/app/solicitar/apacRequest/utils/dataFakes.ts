import { DataApacRequest } from "../contexts/ApacRequestContext";
import { UserRole } from "@/shared/schemas/user";
import { proceduresFakeList } from "@/shared/utils/procedureFakeList";
import { establishmentFakeList } from "@/shared/utils/establishmentFakeList";
import { RequestForm } from "../schemas/requestForm";
import { fakeProcedureOne } from "@/shared/utils/procedureFakeList";

export const fakeRequestForm: RequestForm = {
    requesterId: 42,
    establishmentId: 1,
    apacData: {
    patientName: "João da Silva",
    patientRecordNumber: "2023100456",
    patientCns: "898001160651234",
    patientCpf: "187.149.337-48",
    patientBirthDate: "12/03/1999",
    patientRaceColor: "parda",
    patientGender: "masculino",
    patientMotherName: "Maria Aparecida da Silva",
    patientAddressStreetType: "Avenida",
    patientAddressStreetName: "Abilio Augusto Tavora",
    patientAddressNumber: "2789",
    patientAddressComplement: "Apartamento 201",
    patientAddressPostalCode: "26265-090",
    patientAddressNeighborhood: "Jardim Alvorada",
    patientAddressCity: "Nova Iguaçu",
    patientAddressState: "RJ",
    medicName: "Joseando Pereira",
    medicCns: "1436579",
    medicCbo: "3004894",
    cidId: 1,
    procedureDate: "11/06/2025",
    mainProcedureId: 1,
    subProcedures: [
      {procedure: fakeProcedureOne, checked: true, quantity: 1}
    ]
    }
};

export const fakeDataRequestFillingPart: RequestForm = {
  requesterId: 0,
  establishmentId: 0,
  apacData: {
    patientName: "João da Silva",
    patientRecordNumber: "2023100456",
    patientCns: "898001160651234",
    patientCpf: "187.149.337-48",
    patientBirthDate: "12/03/1999",
    patientRaceColor: "parda",
    patientGender: "masculino",
    patientMotherName: "Maria Aparecida da Silva",
    patientAddressStreetType: "Avenida",
    patientAddressStreetName: "Abilio Augusto Tavora",
    patientAddressNumber: "2789",
    patientAddressComplement: "Apartamento 201",
    patientAddressPostalCode: "26265-090",
    patientAddressNeighborhood: "Jardim Alvorada",
    patientAddressCity: "Nova Iguaçu",
    patientAddressState: "RJ",
    medicName: "Joseando Pereira",
    medicCns: "1436579",
    medicCbo: "3004894",
    cidId: 0,
    procedureDate: "11/06/2025",
    mainProcedureId: 0,
    subProcedures: []
  }
};

