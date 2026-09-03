import Cid from "./cid";

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
    children: Procedure[]; // se estiver populando o related_name
    description?: string | null;
    created_at: string; // datetime em formato ISO (ex: "2025-05-23T12:34:56Z")
    updated_at: string;
    id: number; // assumindo que o modelo Django tem um campo 'id' padrão
}