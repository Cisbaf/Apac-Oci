"use client";
import React from "react";
import ApacFilter from "@/shared/components/ApacFilter";
import ApacTable from "@/shared/components/ApacTable";
import ApacViewProvider from "@/shared/context/ApacViewContext";
import { AuthorizationProvider } from "../responder/apacAuthorization/context/authorizationContext";
import { Box } from "@mui/material";
import AutorizeMultiplesApacProvider from "@/shared/context/AutorizeMultiplesApac";

export default function ApacViewPage() {
    return(
         <Box sx={{ display: "flex", flexDirection: "column", width: "100%", overflow: "auto"}}>
            <ApacViewProvider>
                <AuthorizationProvider>
                <AutorizeMultiplesApacProvider>
                    <ApacFilter/>
                    <ApacTable onlyView/>
                </AutorizeMultiplesApacProvider>
                </AuthorizationProvider>
            </ApacViewProvider>
        </Box>
      
    )
}