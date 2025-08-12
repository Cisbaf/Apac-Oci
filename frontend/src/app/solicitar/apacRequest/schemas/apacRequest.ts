import { User, Establishment, City, Procedure, Cid } from "@/shared/schemas"


export enum ApacStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
}

export const ApacStatusTranslation: Record<ApacStatus, string> = {
  [ApacStatus.PENDING]: 'Pendente',
  [ApacStatus.APPROVED]: 'Aprovado',
  [ApacStatus.REJECTED]: 'Rejeitado',
};

interface SubProcedure {
    procedure: Procedure;
    quantity: number;
    id: number;
}

export interface PatientData {
  name: string;
  record_number: string;
  cns: string;
  cpf: string;
  birth_date: string; // ISO date string (ex: "2025-01-01")
  race_color: string;
  gender: string;
  mother_name: string;
  address_street_type: string;
  address_street_name: string;
  address_number: string;
  address_complement: string;
  address_postal_code: string;
  address_neighborhood: string;
  address_city: string;
  address_state: string;
}

export interface MedicData {
  name: string;
  cns: string;
  cbo: string;
}

export interface ApacData {
  patient_data: PatientData;
  supervising_physician_data: MedicData;
  authorizing_physician_data: MedicData;
  cid: Cid;
  procedure_date: string;
  discharge_date: string;
  main_procedure: Procedure;
  sub_procedures: SubProcedure[];
}
export type ApacRequest = {
    establishment: Establishment;
    requester: User;
    apac_data: ApacData;
    status: ApacStatus;
    request_date: string;
    authorizer: User;
    justification: string;
    review_date: string;
    id: number;
}