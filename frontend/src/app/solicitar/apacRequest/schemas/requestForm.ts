import { Procedure } from "@/shared/schemas";

export interface SubProceduresForm {
  procedure: Procedure;
  quantity: number;
  checked: boolean;
}

export  interface ApacData {
    patientName: string;             // Nome do paciente
    patientRecordNumber: string;           // Nº do prontuário
    patientCns: string;             // CNS do paciente
    patientCpf: string;             // CPF do paciente
    patientBirthDate: string;              // Data de Nascimento
    patientRaceColor: string;              // Raça/Cor
    patientGender: string;      // Sexo do Paciente
    patientMotherName: string;            // Nome da Mãe
    patientAddressStreetType: string;      // Tipo Logradouro (e.g., "TRAVESSA")
    patientAddressStreetName: string;      // Logradouro (e.g., "JOSÉ GOMES TALARICO")
    patientAddressNumber: string;          // Número (e.g., "06")
    patientAddressComplement: string;      // Complemento (e.g., "CASA")
    patientAddressPostalCode: string;      // CEP (e.g., "22221036")
    patientAddressNeighborhood: string;    // Bairro (e.g., "CATETE")
    patientAddressCity: string;            // Município (e.g., "RIO DE JANEIRO")
    patientAddressState: string;           // UF (e.g., "RJ")
    supervisingPhysicianName: string;
    supervisingPhysicianCns: string;
    supervisingPhysicianCbo: string;
    authorizingPhysicianName: string;
    authorizingPhysicianCns: string;
    authorizingPhysicianCbo: string;
    cidId: number;
    procedureDate: string;
    mainProcedureId: number;
    subProcedures: SubProceduresForm[];
}


export interface RequestForm {
    requesterId: number;
    establishmentId: number;
    apacData: ApacData;
}
