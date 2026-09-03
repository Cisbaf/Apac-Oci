import Cid from "./cid";

// Regra "exige ao menos N destes M" (atributos SIGTAP 057, 067-070, T-040).
// member_ids referencia os `id` de `Procedure.children` — o formulário casa
// os dois pra saber quais checkboxes satisfazem qual grupo.
export interface RequirementGroup {
    id: number;
    description: string;
    minimum: number;
    member_ids: number[];
}

export default interface Procedure {
    name: string;
    code: string;
    // T-037: obrigatório e quantidade máxima são do par principal×secundário,
    // não do procedimento — só vêm preenchidos quando este objeto aparece
    // dentro de `children` (a API injeta os dois a partir do vínculo). Ausentes
    // no procedimento principal do topo da lista.
    mandatory?: boolean;
    max_quantity?: number | null;
    is_active: boolean;
    cid: Cid[];
    // Atributo SIGTAP 043 (T-036): quando true, o formulário deve cobrar um
    // segundo CID (causas associadas), escolhido entre `secondary_cids`.
    requires_secondary_cid: boolean;
    secondary_cids: Cid[];
    requirement_groups: RequirementGroup[];
    children: Procedure[]; // se estiver populando o related_name
    description?: string | null;
    created_at: string; // datetime em formato ISO (ex: "2025-05-23T12:34:56Z")
    updated_at: string;
    id: number; // assumindo que o modelo Django tem um campo 'id' padrão
}