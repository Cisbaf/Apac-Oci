import React from "react";
import { ApacBatch } from "../schemas/apacBatch";
import { GetBatchsAvailable } from "../controllers/GetBatchsAvailable";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";


export default function useBatchsList() {
    const [batchs, setBatchs] = React.useState<ApacBatch[]>([]);

    return {batchs, setBatchs};
}