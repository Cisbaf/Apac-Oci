"use client";

import ApacFicha from "@/shared/components/ApacFicha";
import { ApacRequest, ApacStatus } from "../solicitar/apacRequest/schemas/apacRequest";
import { UserRole } from "@/shared/schemas/user";

export const mockApacRequest: ApacRequest = {
  id: 1,
  status: ApacStatus.PENDING,
  request_date: "2025-07-15",
  review_date: "2025-07-20",
  justification: `Paciente apresenta sintomas compatíveis com alterações mamárias. 
Solicita-se realização de mamografia e consulta especializada para confirmação diagnóstica.`,
  
  // Usuário que solicitou
  requester: {
    id: 1,
    name: "MARIA SILVA",
    role: UserRole.REQUESTER,
    city: {
      id: 101,
      name: "Nova Iguaçu"
    }
  },

  // Usuário que autorizou
  authorizer: {
    id: 2,
    name: "JOÃO PAULO",
    role: UserRole.AUTHORIZER,
    city: {
      id: 102,
      name: "Rio de Janeiro"
    }
  },

  // Estabelecimento de saúde
  establishment: {
    id: 1,
    name: "Hospital Municipal São Lucas",
    cnes: "7890380",
    city: {
      id: 102,
      name: "Rio de Janeiro"
    },
    is_active: true
  },

  // Dados da APAC
  apac_data: {
    patient_name: "DANIEL FERNANDES PEREIRA",
    patient_record_number: "887784512",
    patient_cns: "701 8052 0927 4077",
    patient_cpf: "187.149.337-48",
    patient_birth_date: "1999-03-12",
    patient_race_color: "Branca",
    patient_gender: "Masculino",
    patient_mother_name: "FERNANDA RODRIGUES FERNANDES",
    patient_address_street_type: "Rua",
    patient_address_street_name: "KATIA",
    patient_address_number: "200",
    patient_address_complement: "CASA LT",
    patient_address_postal_code: "26261-360",
    patient_address_neighborhood: "COMENDADOR SOARES",
    patient_address_city: "Nova Iguaçu",
    patient_address_state: "RJ",

    // Médico solicitante
    medic_name: "FABRICIO TEIXEIRA DE MELO",
    medic_cns: "709 2092 4674 1133",
    medic_cbo: "545478879",

    // CID
    cid: {
      id: 1,
      code: "N60",
      name: "Displasias mamárias benignas",
      procedure: 1
    },

    procedure_date: "2025-07-15",

    // Procedimento principal
    main_procedure: {
      id: 101,
      name: "OCI AVALIAÇÃO DIAGNÓSTICA INICIAL DE CÂNCER DE MAMA",
      code: "0901010014",
      mandatory: true,
      is_active: true,
      cid: [
    
      ],
      children: [],
      created_at: "2025-01-10T10:00:00Z",
      updated_at: "2025-01-10T10:00:00Z",
      description: null
    },

    // Procedimentos secundários
    sub_procedures: [
      {
        id: 1,
        quantity: 1,
        procedure: {
          id: 102,
          name: "CONSULTA E/OU TELECONSULTA MÉDICA EM ATENÇÃO ESPECIALIZADA",
          code: "0301010021",
          mandatory: false,
          is_active: true,
          cid: [],
          children: [],
          created_at: "2025-01-12T12:00:00Z",
          updated_at: "2025-01-12T12:00:00Z",
          description: null
        }
      },
      {
        id: 2,
        quantity: 1,
        procedure: {
          id: 103,
          name: "MAMOGRAFIA",
          code: "0202020030",
          mandatory: false,
          is_active: true,
          cid: [],
          children: [],
          created_at: "2025-01-15T09:00:00Z",
          updated_at: "2025-01-15T09:00:00Z",
          description: null
        }
      }
    ]
  }
};


export default function TestingPage() {
    return (
        <ApacFicha data={mockApacRequest}/>
    )
}