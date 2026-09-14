import { validatePmae, validateSubProcedures } from "../components/forms/validates/validateSubProcedures";
import { SubProceduresForm } from "../schemas/requestForm";
import Procedure, { RequirementGroup } from "@/shared/schemas/procedure";

/**
 * Regra PMAE (atributo SIGTAP 053) no formulário. Sem ela a APAC de OCI sai em
 * estado que o APAC Magnético recusa com
 * "PMAE EXIGE PELO MENOS 2 PROC.SEC. SENDO UM OBRIG.(030101007 OU 030101030)".
 *
 * O primeiro bloco é da T-042, quando a exigência era um grupo cadastrado por
 * OCI — continua valendo, porque grupo de exigência segue existindo para os
 * atributos 057/067-070. O segundo é a T-043, que derivou a regra do atributo
 * e passou a cobrar também o mínimo de dois secundários, que o grupo nunca
 * cobriu.
 */

function procedimento(id: number, name: string, mandatory = false, code = ""): Procedure {
  return {
    id,
    name,
    code: code || String(id),
    pmae: false,
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

const TOMOGRAFIA = procedimento(1, "Tomografia Computadorizada de Tórax", true, "0206020031");
const CONSULTA = procedimento(2, "Consulta Médica em Atenção Especializada", false, "0301010072");
const TELECONSULTA = procedimento(3, "Teleconsulta Médica na Atenção Especializada", false, "0301010307");
const BACILOSCOPIA = procedimento(4, "Baciloscopia Direta para BAAR", false, "0202080048");

/** OCI de Infectologia: tem o atributo 053 e aceita consulta e teleconsulta. */
const OCI_PMAE: Procedure = {
  ...procedimento(99, "OCI Avaliação Diagnóstica Inicial de Síndromes Respiratórias", false, "0908010010"),
  pmae: true,
  children: [TOMOGRAFIA, CONSULTA, TELECONSULTA, BACILOSCOPIA],
};

/** Saúde Bucal: tem o atributo 053, mas no SIGTAP não tem consulta médica
 *  entre os secundários — só o mínimo de 2 pode ser cobrado dela. */
const OCI_SEM_CONSULTA: Procedure = {
  ...procedimento(98, "OCI Atenção em Saúde Bucal", false, "0907010016"),
  pmae: true,
  children: [TOMOGRAFIA, BACILOSCOPIA],
};

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


describe("validatePmae — regra derivada do atributo 053 (T-043)", () => {
  it("bloqueia a OCI com um secundário só", () => {
    const erro = validatePmae([item(TOMOGRAFIA, true)], OCI_PMAE);

    expect(erro).toContain("pelo menos 2");
  });

  it("bloqueia a OCI só com a consulta — o caso de 6 OCIs em produção", () => {
    const erro = validatePmae([item(CONSULTA, true)], OCI_PMAE);

    expect(erro).toContain("pelo menos 2");
  });

  it("bloqueia dois secundários sem consulta nem teleconsulta", () => {
    const erro = validatePmae([item(TOMOGRAFIA, true), item(BACILOSCOPIA, true)], OCI_PMAE);

    expect(erro).toContain("0301010072");
  });

  it("aceita tomografia + consulta", () => {
    expect(validatePmae([item(TOMOGRAFIA, true), item(CONSULTA, true)], OCI_PMAE)).toBeNull();
  });

  it("aceita tomografia + teleconsulta", () => {
    expect(validatePmae([item(TOMOGRAFIA, true), item(TELECONSULTA, true)], OCI_PMAE)).toBeNull();
  });

  it("não cobra consulta de OCI que não tem consulta entre os secundários", () => {
    expect(validatePmae([item(TOMOGRAFIA, true), item(BACILOSCOPIA, true)], OCI_SEM_CONSULTA)).toBeNull();
  });

  it("mas ainda cobra os 2 secundários dessa OCI", () => {
    expect(validatePmae([item(TOMOGRAFIA, true)], OCI_SEM_CONSULTA)).toContain("pelo menos 2");
  });

  it("não se aplica a procedimento sem o atributo", () => {
    const semAtributo = { ...OCI_PMAE, pmae: false };

    expect(validatePmae([item(TOMOGRAFIA, true)], semAtributo)).toBeNull();
  });
});

describe("validateSubProcedures — regra PMAE junto com o resto", () => {
  it("propaga a violação do PMAE quando o principal é informado", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, true), item(CONSULTA, false)], [], OCI_PMAE
    );

    expect(resultado.success).toBe(false);
    expect(resultado.message).toContain("pelo menos 2");
  });

  it("passa com o pacote mínimo completo", () => {
    const resultado = validateSubProcedures(
      [item(TOMOGRAFIA, true), item(CONSULTA, true)], [], OCI_PMAE
    );

    expect(resultado.success).toBe(true);
  });
});
