import Cid from "./cid";

export default interface Procedure {
    name: string;
    code: string;
    mandatory: boolean;
    is_active: boolean;
    cid: Cid[];
    children: Procedure[]; // se estiver populando o related_name
    description?: string | null;
    created_at: string; // datetime em formato ISO (ex: "2025-05-23T12:34:56Z")
    updated_at: string;
    id: number; // assumindo que o modelo Django tem um campo 'id' padrão
}