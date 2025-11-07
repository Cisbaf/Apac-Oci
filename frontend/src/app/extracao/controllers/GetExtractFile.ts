import { ExtractFormData } from "../schemas/extractForm";
import { formatDateToYMD } from "@/app/solicitar/apacRequest/utils/dateUtils";

export default async function GetExtractFile(data: ExtractFormData) {
    data.production.setDate(1)
    const newData = {
        production: formatDateToYMD(data.production),
        establishment_id: data.establishmentId,
        apac_batchs: data.apacBatchs
    };

    console.log(newData)

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
