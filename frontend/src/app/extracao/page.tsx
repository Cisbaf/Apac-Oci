"use client";
import { Box, Divider, Typography } from "@mui/material"
import { ExportContextProvider } from "./contexts/ExportContext";
import BatchTable from "./components/BatchTable";
import { PlaylistAddCheck } from "@mui/icons-material";
import FilterApacForExtract from "./components/FilterApac";


export default function ExtracaoPage() {

    return (
        <ExportContextProvider>
            <Box sx={{
                display: "flex",
                flexDirection: "column",
                gap: 2
            }}>
                <Box sx={{ display: "flex", alignItems: "center", gap: 4}}>
                    <PlaylistAddCheck sx={{fontSize: 32}}/>
                    <Typography variant='h6'>Extrair APAC OCI</Typography>
                </Box>
                <Divider sx={{mt: 1, mb: 2}}/>
                <FilterApacForExtract/>
                <BatchTable/>
            </Box>
        </ExportContextProvider>
    );
}