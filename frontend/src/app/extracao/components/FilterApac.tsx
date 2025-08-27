import { Button, Grid } from "@mui/material";
import SelectEstablishment from "./SelectEstablishment";
import MonthYearInput from "./MonthYearInput";
import { useExportContext } from "../contexts/ExportContext";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";
import { GetBatchsAvailable } from "../controllers/GetBatchsAvailable";


export default function FilterApacForExtract() {
    const { hookBatchsList, hookExtractForm } = useExportContext();
    const { showAlert, showBackdrop } = useGlobalComponents();

    const SearchBatchs = async() => {
        const form = hookExtractForm.getValues();

        if (form.establishmentId < 1) {
            showAlert({message: "Selecione um estabelecimento!", color: "error"})
            return null;
        }

        showBackdrop(true, "Buscando registros...");

        try {
            const data = await GetBatchsAvailable(form);

            if (!data || data.length < 1) {
                showAlert({message: `Nenhum registro encontrado!`, color: "error"})
            } else {
                showAlert({message: `${data.length} registros encontrado!`, color: "info"})
            }
            
            hookBatchsList.setBatchs(data);
        } catch (err) {
            showAlert({message: String(err), color: "error"})
        } finally {
            showBackdrop(false);
        }
    }

    return (
        <Grid container spacing={3}>
            <Grid size={{lg: 6}}>
                <SelectEstablishment/>
            </Grid>
            <Grid size={{lg: 3}}>
                <MonthYearInput/>
            </Grid>
            <Grid size={{lg: 3}}>
                <Button
                    sx={{display: "flex"}}
                    variant="contained"
                    onClick={SearchBatchs}>Procurar</Button>
            </Grid>
        </Grid>
    )
}