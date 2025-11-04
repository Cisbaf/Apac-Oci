import { PatientInfo } from '../schemas/patientInfo';
import { UseFormSetValue } from 'react-hook-form';
import { RequestForm } from '../schemas/requestForm';

// Utilitário para converter data de "YYYYMMDDhhmmss" → "DD/MM/YYYY"
function formatDate(dateStr?: string | null): string {
  if (!dateStr || dateStr.length < 8) return '';
  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  const day = dateStr.substring(6, 8);
  return `${day}/${month}/${year}`;
}

// Utilitário para converter sexo
function formatGender(gender?: string | null): string {
  return gender === 'M' ? 'masculino' : gender === 'F' ? 'feminino' : '';
}

export function formatCpf(cpf: string | null | undefined): string {
  if (!cpf) return '';
  const digits = cpf.replace(/\D/g, '');
  if (digits.length !== 11) return cpf;
  return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9, 11)}`;
}

export function formatCns(cns: string | null | undefined) {
  if (!cns) return '';
  const digits = cns.replace('/\D/g', '');
  if (digits.length !== 15) return '';
  return `${digits.slice(0, 3)} ${digits.slice(3, 7)} ${digits.slice(7, 11)} ${digits.slice(11, 15)}`;
}

export function formatCep(cep: string | null | undefined): string {
  if (!cep) return '';
  const digits = cep.replace(/\D/g, '');
  if (digits.length !== 8) return cep;
  return `${digits.slice(0, 5)}-${digits.slice(5, 8)}`;
}

function raceToCode(code?: string | null): string {
  const map: Record<string, string> = {
    "01": "branca",
    "02": "preta",
    "03": "parda",
    "04": "amarela",
    "05": "indígena",
    "06": "sem informação",
  };
  return code ? map[code] || '' : '';
}

// Função principal que preenche o formulário diretamente
export function fillRequestFormFromPatient(
  patientInfo: PatientInfo,
  setValue: UseFormSetValue<RequestForm>
): void {
  const { address } = patientInfo;

  // Dados pessoais básicos
  setValue('apacData.patientName', patientInfo.full_name || '');
  setValue('apacData.patientCpf', formatCpf(patientInfo.cpf));
  setValue('apacData.patientCns', formatCns(patientInfo.cns) || '');
  setValue('apacData.patientBirthDate', formatDate(patientInfo.birth_date));
  setValue('apacData.patientGender', patientInfo.gender);
  setValue('apacData.patientMotherName', patientInfo.mother_name || '');

  const raceLabel = raceToCode(patientInfo.race);
  if (patientInfo.race && raceLabel && patientInfo.race !== '06') {
    setValue('apacData.patientRaceColor', patientInfo.race);
  } else {
    // Limpa o campo se for "sem informação"
    setValue('apacData.patientRaceColor', '');
  }

  // Dados de endereço
  if (address) {
    setValue('apacData.patientAddressStreetName', address.street || '');
    setValue('apacData.patientAddressNumber', address.number || '');
    setValue('apacData.patientAddressComplement', address.complement || '');
    setValue('apacData.patientAddressPostalCode', formatCep(address.postal_code));
    setValue('apacData.patientAddressNeighborhood', address.neighborhood || '');
    // setValue('apacData.patientAddressCity', getCityNameByCode(address.city_code) || '');
    setValue('apacData.patientAddressState', address.state || '');
  }
}

// Função auxiliar para converter código IBGE em nome da cidade
function getCityNameByCode(cityCode?: string | null): string {
  // Implementação real precisaria de um dicionário ou API de consulta
  return cityCode ? 'Nome da Cidade' : '';
}