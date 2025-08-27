import { ToSnakeCase } from "@/shared/utils/snakeCase";
import { ExtractFormData } from "../schemas/extractForm";
import { formatDateToISO } from "@/app/solicitar/apacRequest/utils/adapterForm";
import { formatDateToYMD } from "@/app/solicitar/apacRequest/utils/dateUtils";



export default async function GetExtractFile(data: ExtractFormData) {
    const newData = {
        production: formatDateToYMD(data.production),
        establishment_id: data.establishmentId,
        apac_batchs: data.apacBatchs
    };

    const response = await fetch("/api/proxy/apac_batch/extract", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(newData),
    });

    const json = await response.json();

    if (!response.ok) {
        throw new Error(json.message);
    };

    return json;
}
