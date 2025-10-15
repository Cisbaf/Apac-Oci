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
                gap: 2,
                pt: 1
            }}>
                <FilterApacForExtract/>
                <BatchTable/>
            </Box>
        </ExportContextProvider>
    );
}