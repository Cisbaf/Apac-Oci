import { Establishment } from "@/shared/schemas";
import React from "react";
import { GetEstablishments } from "../controllers/GetEstablishment";
import { useExportContext } from "../contexts/ExportContext";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { Controller } from 'react-hook-form';


export default function SelectEstablishment() {
    const { hookExtractForm } = useExportContext();
    const [establishments, setEstablishments] = React.useState<Establishment[]>([]);

    React.useEffect(()=>{
        GetEstablishments()
        .then(list=>setEstablishments(list));
    }, [])

    React.useEffect(()=>{
        const v = hookExtractForm.establishmentIdValue;
        if (!v) return;
        const establishment = establishments.find(e=>e.id === v);
        if (!establishment) throw new Error("establishmentName não encontrado!");
        hookExtractForm.setEstablishmentName(establishment.acronym);
    }, [hookExtractForm.establishmentIdValue]);

    return (
        <Controller
            name="establishmentId"
            control={ hookExtractForm.control }
            render={({ field }) => (
            <FormControl fullWidth>
                <InputLabel id="establishment-select-label">
                    Estabelecimento
                </InputLabel>
                <Select
                data-testid="select-establishment"
                id="establishment-select"
                label="Nome do estabelecimento de Saúde"
                required
                {...field}>
                <MenuItem value={0} disabled>
                    <em>Selecione um Estabelecimento</em>
                </MenuItem>
                {establishments.map(establishment=>(
                <MenuItem 
                    key={establishment.cnes}
                    value={establishment.id}
                    >
                    {establishment.name}
                </MenuItem>
                ))}
                </Select>
            </FormControl>
    )}/>
    )


}