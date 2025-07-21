import { Procedure } from "../schemas";

const baseDate = "2025-01-01T00:00:00Z";

// Primeiro, criamos os procedimentos sem `parent`
export const fakeProcedureOne: Procedure = {
  id: 1,
  code: "0005010035",
  name: "OCI MUALAÇÃO INICIAL EM OFFICIALOLOGIA",
  mandatory: false,
  cid: [{id: 1, name: "teste", code: "#teste", procedure: 1}],
  children: [
    {
      id: 2,
      code: "02010100072",
      name: "CONSULTA IMEDICA EM ATENÇÃO ESPECIALIZADA",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    },
    {
      id: 3,
      code: "0211060009",
      name: "BOMBOBOSCOPIA DE FLARO DE OLHO",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    },
    {
      id: 4,
      code: "0211060127",
      name: "MAPEJAMENTO DE RETINA",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    }
  ],
  description: null,
  is_active: true,
  created_at: baseDate,
  updated_at: baseDate,
};



export const fakeProcedureTwo: Procedure = {
  id: 7,
  code: "0302010001",
  name: "EXAME COMPLETO DE NEUROCIÊNCIA APLICADA",
  mandatory: false,
  cid: [],
  children: [
    {
      id: 8,
      code: "0302010002",
      name: "ANÁLISE COGNITIVA FUNCIONAL",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    },
    {
      id: 9,
      code: "0302010003",
      name: "MAPEAMENTO DE ATIVIDADE NEURONAL",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    },
    {
      id: 10,
      code: "0302010004",
      name: "TESTE DE RESPOSTA SINÁPTICA",
      mandatory: false,
      cid: [],
      children: [],
      description: null,
      is_active: true,
      created_at: baseDate,
      updated_at: baseDate,
    }
  ],
  description: null,
  is_active: true,
  created_at: baseDate,
  updated_at: baseDate,
};


export const proceduresFakeList: Procedure[] = [
  fakeProcedureOne,
  fakeProcedureTwo,
];
