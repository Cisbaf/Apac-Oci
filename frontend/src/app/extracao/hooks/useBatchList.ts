import React from "react";
import { ApacBatch } from "../schemas/apacBatch";

export default function useBatchsList() {
    const [batchs, setBatchs] = React.useState<ApacBatch[]>([]);

    return {batchs, setBatchs};
}