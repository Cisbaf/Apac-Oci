import { useForm } from "react-hook-form";
import { ExtractFormData } from "../schemas/extractForm";

export default function useExtractForm() {
    const form = useForm<ExtractFormData>({
        defaultValues: {apacBatchs: [], production: new Date(), establishmentId: 0, establishmentName: ""},
    });

    const { getValues, setValue, watch, control } = form;

    const productionValue = watch("production");
    const batchsSelected = watch("apacBatchs");
    const establishmentIdValue = watch("establishmentId");

    const addBatchId = (id: number) => {
        const current = getValues("apacBatchs") || [];
        if (!current.includes(id)) {
            setValue("apacBatchs", [...current, id], { shouldValidate: true, shouldDirty: true });
        }
     };

    const removeBatchId = (id: number) => {
        const current = getValues("apacBatchs") || [];
        setValue(
            "apacBatchs",
            current.filter((batchId) => batchId !== id)
        );
    }

    const setProduction = (date: Date) => {
        setValue("production", date);
    };

    const setEstablishmentName = (name: string)=> {
        setValue("establishmentName", name);
    }


    return {addBatchId, removeBatchId, setProduction, productionValue, control, setEstablishmentName, batchsSelected, getValues, establishmentIdValue}

}