import { ApacRequest } from "@/app/solicitar/apacRequest/schemas/apacRequest";
import { City } from "@/shared/schemas";


interface Validity {
    expire_in: Date;
    created_in: string;
}

export interface ApacBatch {
    batch_number: string;
    city: City;
    validity: Validity;
    apac_request: ApacRequest;
    export_date?: Date;
    id: number;
}