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

export interface ApacData {
  patient_name: string;
  patient_record_number: string;
  patient_cns: string;
  patient_cpf: string;
  patient_birth_date: string;
  patient_race_color: string;
  patient_gender: string;
  patient_mother_name: string;
  patient_address_street_type: string;
  patient_address_street_name: string;
  patient_address_number: string;
  patient_address_complement: string;
  patient_address_postal_code: string;
  patient_address_neighborhood: string;
  patient_address_city: string;
  patient_address_state: string;
  medic_name: string;
  medic_cns: string;
  medic_cbo: string;
  cid: Cid;
  procedure_date: string;
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