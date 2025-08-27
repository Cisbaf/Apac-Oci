import React from "react";
import { TextField } from "@mui/material";
import { useExportContext } from "@/app/extracao/contexts/ExportContext";

const MonthYearInput: React.FC = () => {
    const { hookExtractForm } = useExportContext();
    
    const date = new Date();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const [year, month] = e.target.value.split("-"); // ex: "2025-08" -> ["2025", "08"]
        const date = new Date(Number(year), Number(month) - 1, 1);
        console.log(date);
        hookExtractForm.setProduction(date);
    };

    const fomartInput = (date: Date) => {
        if (!date) return '';
        return `${date.getFullYear()}-0${date.getMonth() + 1}`;
    }

    const valueDate = fomartInput(hookExtractForm.productionValue);

    return (
        <TextField
            sx={{display: "flex"}}
            label="Competência"
            type="month"
            value={valueDate}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }} // mantém o label acima
            inputProps={{ min: `${date.getFullYear()}-01`, max: `${date.getFullYear()}-0${date.getMonth() + 1}` }} // limites opcionais
        />
    );
};

export default MonthYearInput;
