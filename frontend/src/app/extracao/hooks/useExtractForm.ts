import { useForm } from "react-hook-form";
import { ExtractFormData } from "../schemas/extractForm";

export default function useExtractForm() {
    const form = useForm<ExtractFormData>({
        defaultValues: {apacBatchs: [], establishmentId: 0, production: new Date(),},
    });

    const { getValues, setValue, watch, control, trigger } = form;

    const productionValue = watch("production");
    const batchsSelected = watch("apacBatchs");

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

    const setEstablishmentId = (id: number)=> {
        setValue("establishmentId", id);
    }


    return {addBatchId, removeBatchId, setProduction, productionValue, control, setEstablishmentId, batchsSelected, getValues}

}