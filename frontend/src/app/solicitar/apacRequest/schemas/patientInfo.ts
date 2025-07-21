export interface Address {
  street: string;
  number: string;
  complement: string | null;
  neighborhood: string;
  city_code: string;
  state: string | null;
  postal_code: string | null;
  country_code: string;
}

export interface PatientInfo {
  full_name: string;
  social_name: string | null;
  birth_date: string; // formato YYYYMMDDhhmmss
  gender: 'M' | 'F';
  cpf: string | null;
  cns: string | null;
  phone: string | null;
  email: string | null;
  address: Address;
  mother_name: string | null;
  father_name: string | null;
  marital_status: string | null;
  race: string | null;
  ethnicity: string | null;
  deceased: boolean;
  deceased_date: string | null;
  birth_place_city_code: string | null;
  birth_place_country_code: string | null;
  
  // Documentos adicionais
  rg: string | null;
  ctps: string | null;
  cnh: string | null;
  voter_id: string | null;
  nis: string | null;
  passport: string | null;
  ric: string | null;
  dnv: string | null;
  local_id: string | null;
  
  // Flags e informações adicionais
  vip: boolean;
  other_ids: string[];
  additional_info: Record<string, unknown>;
}

export interface CadSUSRequest {
  type_consult: 'cpf' | 'cns';
  value: string;
}