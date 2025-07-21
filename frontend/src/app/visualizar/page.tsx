"use client";
import React from "react";
import ApacFilter from "@/shared/components/ApacFilter";
import ApacTable from "@/shared/components/ApacTable";
import ApacViewProvider from "@/shared/context/ApacViewContext";
import { AuthorizationProvider } from "../responder/apacAuthorization/context/authorizationContext";
import { Box, Typography, Divider } from "@mui/material";
import { PlaylistAddCheck } from "@mui/icons-material";

export default function ApacViewPage() {
    return(
         <Box sx={{ display: "flex", flexDirection: "column"}}>
            <Box sx={{ display: "flex", alignItems: "center", gap: 4}}>
                <PlaylistAddCheck sx={{fontSize: 32}}/>
                <Typography variant='h6'>Visualizar Solicitações APAC OCI</Typography>
            </Box>
            <Divider sx={{mt: 1, mb: 2}}/>
            <ApacViewProvider>
                <AuthorizationProvider>
                    <ApacFilter/>
                    <ApacTable onlyView/>
                </AuthorizationProvider>
            </ApacViewProvider>
        </Box>
      
    )
}