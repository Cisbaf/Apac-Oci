import { validateSubProcedures } from "../components/forms/validates/validateSubProcedures";
import { SubProceduresForm } from "../schemas/requestForm";
import Procedure, { RequirementGroup } from "@/shared/schemas/procedure";

/**
 * T-042 — a regra PMAE (atributo SIGTAP 053) chega ao formulário como um grupo
 * de exigência comum: "pelo menos 1 de [consulta, teleconsulta]". Sem ela, a
 * APAC de OCI sai sem consulta e o APAC Magnético devolve
 * "PMAE EXIGE PELO MENOS 2 PROC.SEC. SENDO UM OBRIG.(030101007 OU 030101030)".
 */

function procedimento(id: number, name: string, mandatory = false): Procedure {
  return {
    id,
    name,
    code: String(id),
    mandatory,
    max_quantity: null,
    is_active: true,
    cid: [],
    requires_secondary_cid: false,
    secondary_cids: [],
    requirement_groups: [],
    children: [],
    created_at: "2026-08-01T00:00:00Z",
    updated_at: "2026-08-01T00:00:00Z",
  };
}

function item(procedure: Procedure, checked: boolean): SubProceduresForm {
  return { procedure, quantity: 1, checked };
}

const TOMOGRAFIA = procedimento(1, "Tomografia Computadorizada de Tórax", true);
const CONSULTA = procedimento(2, "Consulta Médica em Atenção Especializada");
const TELECONSULTA = procedimento(3, "Teleconsulta Médica na Atenção Especializada");

const GRUPO_PMAE: RequirementGroup = {
  id: 10,
  description:
    "Consulta médica em atenção especializada ou teleconsulta médica na atenção especializada (toda APAC de OCI exige uma das duas)",
  minimum: 1,
  member_ids: [CONSULTA.id, TELECONSULTA.id],
};

describe("validateSubProcedures — grupo da consulta (PMAE)", () => {
  it("bloqueia a OCI marcada só com a tomografia", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, true), item(CONSULTA, false), item(TELECONSULTA, false)],
      [GRUPO_PMAE]
    );

    expect(resultado.success).toBe(false);
    expect(resultado.message).toContain("pelo menos 1");
  });

  it("aceita com a consulta marcada", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, true), item(CONSULTA, true), item(TELECONSULTA, false)],
      [GRUPO_PMAE]
    );

    expect(resultado.success).toBe(true);
  });

  it("aceita com a teleconsulta no lugar da consulta", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, true), item(CONSULTA, false), item(TELECONSULTA, true)],
      [GRUPO_PMAE]
    );

    expect(resultado.success).toBe(true);
  });

  it("cobra o secundário obrigatório antes do grupo", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, false), item(CONSULTA, true)],
      [GRUPO_PMAE]
    );

    expect(resultado.success).toBe(false);
    expect(resultado.message).toContain(TOMOGRAFIA.name);
  });
});
